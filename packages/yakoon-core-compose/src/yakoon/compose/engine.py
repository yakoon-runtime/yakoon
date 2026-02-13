from yakoon.base import ports
from yakoon.base.descriptors.template import TemplateSource
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.catalog import CommandInfo, ControllerInfo
from yakoon.base.stores.base.registry import StoreRegistry
from yakoon.platform.directories.controller import ControllerDirectory
from yakoon.platform.engines.command.engine import Engine
from yakoon.platform.engines.command.router import CommandDirectory, CommandRouter
from yakoon.platform.runtime.render.jinja.engine import JinjaEngine
from yakoon.platform.services.account import AccountService
from yakoon.platform.services.auditlog import AuditLogService
from yakoon.platform.services.auth import AuthenticationService, ZeroSecretVerifier
from yakoon.platform.services.catalog import (
    CommandCatalog,
    CommandCatalogService,
    ControllerCatalog,
    ControllerCatalogService,
)
from yakoon.platform.services.command import CommandQueueService
from yakoon.platform.services.dialogservice import DefaultDialogService
from yakoon.platform.services.namespace import NamespaceService
from yakoon.platform.services.perm import PermissionService
from yakoon.platform.services.presenter import PresenterService
from yakoon.platform.services.prompt import PromptService
from yakoon.platform.services.render import RendererService
from yakoon.platform.services.session import SessionService
from yakoon.platform.services.shard import ShardAllocator, ShardedCounterService
from yakoon.platform.stores.factory import create_system_stores
from yakoon.platform.stores.memory.account import InMemoryAccountStore
from yakoon.workflow.services.compile import WorkflowCompileService
from yakoon.workflow.services.engine import WorkflowService


def compose_engine(controllers: ControllerDirectory) -> Engine:

    command_catalog = _compose_command_catalog(controllers)
    controller_catalog = _compose_controller_catalog(controllers)

    stores = _compose_stores()
    commands = _compose_commands(controllers)
    templates = _compose_template_sources(controllers)

    services = _compose_services(stores, controller_catalog, command_catalog, templates)

    _compose_controllers(controllers, services)
    _compose_permission_roles(services)

    engine = Engine(controllers, services, commands)

    return engine


def _compose_permission_roles(services: ServiceDirectory):

    permissions = services.get(ports.PermissionService)
    permissions.register_role(
        "admin",
        [
            "auth:su|rx",
            "shell:use|rx",
            "office.mailing:sendmail|rx",
        ],
    )
    permissions.register_role(
        "user",
        [
            "shell:use|rx",
        ],
    )


def _compose_controllers(directory: ControllerDirectory, services: ServiceDirectory):

    for controller in directory.get_all():
        controller.connect_services(services.fork())


def _compose_controller_catalog(directory: ControllerDirectory) -> ControllerCatalog:

    controllers_list = []
    for controller in directory.get_all():
        controller_info = ControllerInfo(
            controller.id,
            controller.is_shell,
            controller.is_activatable,
            controller.is_listed,
            controller.template_source.clone(),
            controller.workflow_source.clone(),
        )
        controllers_list.append(controller_info)

    return ControllerCatalog(controllers_list)


def _compose_command_catalog(directory: ControllerDirectory) -> CommandCatalog:

    shell_builtins = {}
    command_list = []
    for controller in directory.get_all():
        if controller.is_shell:
            shell_builtins = controller.shell_builtins
        for sets in controller.commandsets:
            for command in sets.commands():
                command_info = CommandInfo(
                    command.key,
                    command.kind,
                    command.visibility,
                    sets.group,
                    controller.id,
                    command.template_prefix,
                )
                command_list.append(command_info)

    return CommandCatalog(command_list, shell_builtins)


def _compose_commands(directory: ControllerDirectory) -> CommandDirectory:

    commands = CommandDirectory()
    for controller in directory.get_all():
        router = CommandRouter(
            controller.id,
            controller.is_shell,
            controller.is_listed,
            controller.is_activatable,
            controller.shell_builtins,
        )

        router.register(controller.id, controller.commandsets)
        commands.register(controller.id, router)

    return commands


def _compose_services(
    stores: StoreRegistry,
    controller_catalog: ControllerCatalog,
    command_catalog: CommandCatalog,
    template_sources: list[TemplateSource],
) -> ServiceDirectory:

    services = ServiceDirectory()

    services.register_static(ports.AuditLogService, AuditLogService())
    services.register_static(ports.NamespaceService, NamespaceService())
    services.register_static(ports.SessionService, SessionService(stores.sessions))
    services.register_static(ports.CommandQueueService, CommandQueueService())
    services.register_static(ports.PresenterService, PresenterService(services))
    services.register_static(ports.PromptService, PromptService(services))
    services.register_static(
        ports.AccountService, AccountService(InMemoryAccountStore())
    )
    services.register_static(ports.SecretVerifier, ZeroSecretVerifier())
    services.register_static(
        ports.AuthenticationService, AuthenticationService(services)
    )
    services.register_static(ports.PermissionService, PermissionService())
    services.register_static(ports.DialogService, DefaultDialogService())
    services.register_static(ports.WorkflowService, WorkflowService(services))
    services.register_static(ports.WorkflowCompileService, WorkflowCompileService())

    services.register_static(
        ports.RendererService, RendererService(JinjaEngine(template_sources))
    )

    services.register_static(
        ports.ShardedCounterService,
        ShardedCounterService(ShardAllocator(stores.counters)),
    )

    services.register_static(
        ports.ControllerCatalogService, ControllerCatalogService(controller_catalog)
    )

    services.register_static(
        ports.CommandCatalogService, CommandCatalogService(services, command_catalog)
    )

    return services


def _compose_template_sources(directory: ControllerDirectory) -> list[TemplateSource]:

    template_sources: list[TemplateSource] = []

    for controller in directory.get_all():
        template_sources.append(controller.template_source)

    return template_sources


def _compose_stores() -> StoreRegistry:

    stores = create_system_stores("memory", db_path="db/gateway.sqlite3.db")
    return stores
