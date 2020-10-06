__author__ = 'mohamed'


class BaseSCM():
    def get_clone_cmd(self):
        pass
    def get_pull_cmd(self):
        pass
    def get_list_tags_cmd(self):
        pass
    def get_switch_to_tag_cmd(self):
        pass
    def get_history_cmd(self,page=0,rpp=10,options={}):
        pass
    def switch_to_histroy_cmd(self,commit):
        pass
    def commit_diff_cmd(self,commit):
        pass
