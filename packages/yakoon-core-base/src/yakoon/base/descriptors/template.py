from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class TemplateSource:
    """Describes where a controller's templates are located.

    A TemplateSource is a pure configuration object. It does not load or
    resolve templates itself. That responsibility belongs to the presenter
    layer.

    Attributes:
        package:
            Python package used as the loader root (e.g. "yakoon.shell").
        template_path:
            Folder inside the package containing templates.
        template_sub_path:
            Optional namespace prefix below template_path
            (e.g. "core", "system", "crm").
        man_folder:
            Subfolder under template_path used for manual/help templates.

    Design notes:
        - Immutable by design (frozen dataclass).
        - Controller-owned.
        - Pure descriptor, no logic.
    """

    package: str | None
    template_path: str = "templates"
    template_sub_path: str = ""
    man_folder: str = "man"

    def clone(self) -> "TemplateSource":
        """Return a copy of this TemplateSource.

        Useful when a controller needs to derive a modified configuration
        (e.g. adjust sub_path) without mutating the original descriptor.
        """
        return TemplateSource(
            self.package,
            self.template_path,
            self.template_sub_path,
            self.man_folder,
        )
