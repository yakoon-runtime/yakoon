from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class WorkflowSource:
    """Describes where a controller's workflow definitions are located.

    A WorkflowSource is a structural descriptor. It does not interpret
    or execute workflows; it only defines their package root.

    Attributes:
        package:
            Python package used as the workflow loader root.
        workflow_path:
            Folder inside the package containing workflow definitions.
        workflow_sub_path:
            Optional namespace prefix below workflow_path.

    Design notes:
        - Immutable configuration object.
        - Owned by the controller.
        - Resolution logic belongs to the workflow service layer.
    """

    package: str
    workflow_path: str = "workflows"
    workflow_sub_path: str = ""

    def clone(self) -> "WorkflowSource":
        """Return a copy of this WorkflowSource."""
        return WorkflowSource(
            self.package,
            self.workflow_path,
            self.workflow_sub_path,
        )
