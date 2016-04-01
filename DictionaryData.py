class Data:
    def __init__(self, processed, skipped, flat, bound):
        self.processed_files = processed
        self.skipped_files = skipped
        self.rows_flat = flat
        self.rows_bound = bound