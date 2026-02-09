from dataclasses import dataclass


@dataclass(frozen=True)
class WorkflowSource:
    """
    Defines where workflows for a controller are loaded from.

    The Python package name is used as the loader key.
    All template resolution below package_path is purely structural.
    """
    
    package: str                       # Python package name, also used as loader key
    workflow_path: str = "workflows"    # Folder within the package.
    workflow_sub_path: str = ""        # Prefix/Namespace (shell/system)

    def clone(self):        
        
        return WorkflowSource(
            self.package,
            self.workflow_path,
            self.workflow_sub_path)
  