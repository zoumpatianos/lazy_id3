"""
"""

class LazyInformationGain(object):
    
    def __init__(self, dataset, target_value, instance):
        self.dataset = dataset
        self.target_value = target_value
        self.instance = instance

    def make_choice(self, current_index, subset, do_not_expand):
        return 0
