from app.models.focus_level import FocusLevel
from app.models.work_block import WorkBlock


class WorkBlockService:
    def __init__(self, work_blocks: list[WorkBlock] | None = None):
        self.work_blocks = work_blocks or []

    def create_work_block(
        self,
        title,
        start_at,
        end_at,
        focus_level: FocusLevel,
        description=None,
    ):
        work_block = WorkBlock(
            id=self.next_work_block_id(),
            title=title,
            start_at=start_at,
            end_at=end_at,
            focus_level=focus_level,
            description=description,
        )

        self.work_blocks.append(work_block)

        return work_block

    def next_work_block_id(self):
        if not self.work_blocks:
            return 1

        return max(
            work_block.id
            for work_block in self.work_blocks
        ) + 1