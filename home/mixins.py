class SeriesMixin:
    def get_total_episodes_and_duration(self, series):
        # Fetch all seasons for this series
        seasons = series.seasons.all()

        # Initialize totals
        total_duration_seconds = 0
        total_episodes_count = 0

        # Calculate total duration and number of episodes
        for season in seasons:
            # Get the season's total duration and episode count
            total_duration_seconds += season.total_duration_seconds()
            total_episodes_count += season.number_of_episodes()

        # Convert total duration seconds to formatted duration
        total_duration_formatted = self.format_duration(total_duration_seconds)

        return total_episodes_count, total_duration_formatted

    def format_duration(self, total_seconds):
        """ Helper function to format seconds into mm:ss. """
        minutes, seconds = divmod(total_seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"

