from model.goal import Goal


class InMemoryGoalRepository:
    def __init__(self) -> None:
        self._seq = 1
        self._goals: dict[int, Goal] = {}

    def create(self, title: str, owner_id: int) -> Goal:
        goal = Goal(id=self._seq, title=title, owner_id=owner_id)
        self._goals[self._seq] = goal
        self._seq += 1
        return goal

    def list_all(self, owner_id: int) -> list[Goal]:
        return [g for g in self._goals.values() if g.owner_id == owner_id]

