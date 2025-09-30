import os

class Memory:
    def __init__(self):
        self.last_plan = None
        self.last_results = []
        self.last_working_directory = os.getcwd()

    def set_last_plan(self, plan):
        self.last_plan = plan

    def set_last_results(self, results):
        self.last_results = results

    def set_last_working_directory(self, cwd):
        self.last_working_directory = cwd

    def get_last_plan(self):
        return self.last_plan

    def get_last_results(self):
        return self.last_results

    def get_last_working_directory(self):
        return self.last_working_directory

    def resolve_pronoun(self, pronoun):
        """
        Resolves a pronoun to the last results.
        """
        if pronoun.lower() in ['them', 'those', 'those files', 'it']:
            return self.last_results
        return None