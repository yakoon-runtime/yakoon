from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateSource:
    """
    A Template-Root, typical:
      - plugin package + templates folder (PackageLoader)
      - optional: host overrides (FileSystemLoader)
    """
    name: str                           # Namespace / Prefix, z.B. "office.mailing"
    package: str                        # Python package name, z.B. "office_mailing"
    package_path: str = "templates"     # Folder within the package.
