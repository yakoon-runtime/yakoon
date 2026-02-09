from dataclasses import dataclass


@dataclass(frozen=True)
class TemplateSource:
    """
    Defines where templates for a controller are loaded from.

    The Python package name is used as the loader key.
    All template resolution below package_path is purely structural.
    """
    
    package: str                       # Python package name, also used as loader key
    template_path: str = "templates"   # Folder within the package.
    template_sub_path: str = ""        # Prefix/Namespace (shell/system)
    man_folder: str = "man"            # The name under the template_path

    def clone(self):        
        return TemplateSource(
            self.package,
            self.template_path,
            self.template_sub_path, 
            self.man_folder)
  