from yakoon.base import ports
from yakoon.base.directories.service import ServiceDirectory
from yakoon.base.models.fields import FieldSpec


class FieldSpecRenderService:
    """
    Combines policy FieldSpec with rendered UI text.
    """

    def __init__(self, services: ServiceDirectory):
        self._services = services

    async def build(
        self,
        ctx,
        *,
        section_key: str,
        policy: str,
        **data,
    ) -> FieldSpec:

        policies = self._services.get(ports.PolicyService)
        pol = policies.get_policy(policy)

        render_srv = self._services.get(ports.RendererService)
        label = await render_srv.render(ctx, section_key, **data)

        # merge: copy base but override label
        return FieldSpec(
            key=pol.key,
            label=label,
            type=pol.type,
            required=pol.required,
            hint=pol.hint,
            secret=pol.secret,
            options=pol.options,
        )
