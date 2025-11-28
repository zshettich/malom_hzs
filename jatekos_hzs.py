class Playerrankhzs:
    def __init__(self):
        self.results = []

    def add_result_hzs(self, time, winner):
        self.results.append((time, winner))

    def get_sorted_results_hzs(self):
        return sorted(enumerate(self.results), key=lambda x: x[1][0])

    def get_results_text_hzs(self):
        if not self.results:
            return "Még nincs eredmény"

        sorted_results = self.get_sorted_results_hzs()
        relative_ranks = [0] * len(self.results)

        for rank_idx, (original_idx, (time, winner)) in enumerate(sorted_results):
            relative_ranks[original_idx] = rank_idx + 1

        text = "Eredmények:\n"
        for i, (time, winner) in enumerate(self.results):
            winner_text = "Te" if winner == 1 else "Gép"
            rank = relative_ranks[i]
            text += f"{i + 1}. játék: {time} mp, Győztes: {winner_text}, {rank}. helyezés\n"

        return text