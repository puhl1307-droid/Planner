from app.models.focus_level import FocusLevel


class PlanningValidationService:
    def validate_planning_block(
        self,
        planning_block,
        planning_blocks,
        work_blocks,
        tasks,
    ):
        warnings = []

        task = next(
            (
                task
                for task in tasks
                if task.id == planning_block.task_id
            ),
            None,
        )

        work_block = None

        if planning_block.work_block_id is not None:
            work_block = next(
                (
                    work_block
                    for work_block in work_blocks
                    if work_block.id
                    == planning_block.work_block_id
                ),
                None,
            )

        # 1. Zugeordneter WorkBlock existiert nicht
        if (
            planning_block.work_block_id is not None
            and work_block is None
        ):
            warnings.append(
                "Der zugeordnete WorkBlock existiert nicht."
            )

        # 2. PlanningBlock liegt nicht vollständig im WorkBlock
        if work_block is not None:
            if (
                planning_block.start_at
                < work_block.start_at
                or planning_block.end_at
                > work_block.end_at
            ):
                warnings.append(
                    "Der PlanningBlock liegt nicht vollständig "
                    "innerhalb des WorkBlocks."
                )

        # 3. Fokusbedarf des Tasks höher als verfügbarer Fokus
        if (
            task is not None
            and work_block is not None
        ):
            focus_rank = {
                FocusLevel.LOW: 1,
                FocusLevel.MEDIUM: 2,
                FocusLevel.HIGH: 3,
            }

            if (
                focus_rank[task.focus_requirement]
                > focus_rank[work_block.focus_level]
            ):
                warnings.append(
                    "Der Fokusbedarf des Tasks ist höher "
                    "als der verfügbare Fokus im WorkBlock."
                )

        # 4. Überschneidung mit anderem PlanningBlock
        for other in planning_blocks:
            if other.id == planning_block.id:
                continue

            overlaps = (
                planning_block.start_at < other.end_at
                and planning_block.end_at > other.start_at
            )

            if overlaps:
                warnings.append(
                    "Der PlanningBlock überschneidet sich "
                    "mit einem anderen PlanningBlock."
                )
                break

        return warnings