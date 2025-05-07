# This file is the actual code for the Python runnable Helm Runner
import os

from dataiku.runnables import Runnable

from dku_helm.helm_command import Helm

class MyRunnable(Runnable):
    """The base interface for a Python runnable"""

    def __init__(self, project_key, config, plugin_config):
        """
        :param project_key: the project in which the runnable executes
        :param config: the dict of the configuration of the object
        :param plugin_config: contains the plugin settings
        """
        self.project_key = project_key
        self.config = config
        self.plugin_config = plugin_config
        
        self.Helm = Helm()
        
    def get_progress_target(self):
        """
        If the runnable will return some progress info, have this function return a tuple of 
        (target, unit) where unit is one of: SIZE, FILES, RECORDS, NONE
        """
        return None

    def run(self, progress_callback):
        """
        Do stuff here. Can return a string or raise an exception.
        The progress_callback is a function expecting 1 value: current progress
        """
        os.environ["KUBECONFIG"] = self.config.get("kubeConfig")

        op = self.config.get("operator")
        
        if op == "addRepo":
            self.Helm.add_repo(self.config.get("repo"), self.config.get("repoUrl"))
            
        if op == "install":
            self.Helm.install(self.config.get("chartName"), self.config.get("repo"), self.config.get("namespace"))
            
        if op == "removeRepo":
            self.Helm.remove_repo(self.config.get("repo"))
            
        if op == "uninstall":
            self.Helm.uninstall(self.config.get("chartName"), self.config.get("namespace"))
            
        if op == "update":
            self.Helm.update()
            
        if op == "search":
            rt = self.Helm.search(self.config.get("searchTerm"))
            return rt
        
        if op == "deployNimLlms":
            rt = self.Helm.deploy_nim_llm(self.config.get("namespace"), self.config.get("namespace"), self.config.get("namespace"))
            return rt
        
        
        del os.environ["KUBECONFIG"]