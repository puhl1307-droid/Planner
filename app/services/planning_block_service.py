from datetime import datetime

from app.models.planning_block import PlanningBlock


class PlanningBlockService:
    def __init__(
        self,
        planning_blocks: list[PlanningBlock] | None = None,
    ):
        self.planning_blocks = planning_blocks or []

    def create_planning_block(
        self,
        task_id: int,
        start_at: datetime,
        end_at: datetime,
        work_block_id: int | None = None,
    ) -> PlanningBlock:
        planning_block = PlanningBlock(
            id=self.next_planning_block_id(),
            task_id=task_id,
            start_at=start_at,
            end_at=end_at,
            work_block_id=work_block_id,
        )

        self.planning_blocks.append(
            planning_block
        )

        return planning_block

    def next_planning_block_id(self) -> int:
        if not self.planning_blocks:
            return 1

        return (
            max(
                planning_block.id
                for planning_block
                in self.planning_blocks
            )
            + 1
        )