# !/usr/bin/env python
#  -*- coding: UTF-8 -*-
#
#
# ==================
# VIZ HTML MULTI - html visualization with multiple files, one per entity
# ==================

import os, sys
import json

from ..core import *
from ..core.utils import *
from ..core.builder import *  # loads and sets up Django
from ..core.viz_factory import VizFactory





class KompleteViz(VizFactory):
    """

    """


    def __init__(self, ontospy_graph, title="", theme="", text=""):
        """
        Init
        """
        super(KompleteViz, self).__init__(ontospy_graph, title, text)
        self.static_files = [
                "custom",
                "libs/bootswatch3_2",
                "libs/bootstrap-3_3_7-dist",
                "libs/jquery",
                "libs/chartjs-2_4_0",
                "libs/d3-v2"
                ]
        self.theme = validate_theme(theme)
        self.text = text

    def _buildTemplates(self):
        """
        OVERRIDING THIS METHOD from Factory
        """
        # INDEX - MAIN PAGE
        contents = self._renderTemplate("html-multi/index.html", extraContext={"theme": self.theme, "index_page_flag" : True})
        FILE_NAME = "index.html"
        main_url = self._save2File(contents, FILE_NAME, self.output_path)

        # DASHBOARD
        contents = self._renderTemplate("html-multi/statistics.html", extraContext={"theme": self.theme})
        FILE_NAME = "statistics.html"
        self._save2File(contents, FILE_NAME, self.output_path)

        # ILLUSTRATIONS
        contents = self._renderTemplate("html-multi/illustrations.html", extraContext={"theme": self.theme})
        FILE_NAME = "illustrations.html"
        self._save2File(contents, FILE_NAME, self.output_path)

        # VIZ LIST
        if False:
            contents = self._renderTemplate("html-multi/viz_list.html", extraContext={"theme": self.theme})
            FILE_NAME = "visualizations.html"
            self._save2File(contents, FILE_NAME, self.output_path)


        browser_output_path = self.output_path

        # ENTITIES A-Z
        extra_context = {"ontograph": self.ontospy_graph, "theme": self.theme}
        contents = self._renderTemplate("html-multi/browser/browser_entities_az.html", extraContext=extra_context)
        FILE_NAME = "entities-az.html"
        self._save2File(contents, FILE_NAME, browser_output_path)

        c_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayer)
        p_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayerProperties)
        s_mylist = build_D3treeStandard(0, 99, 1, self.ontospy_graph.toplayerSkosConcepts)

        c_total = len(self.ontospy_graph.classes)
        p_total = len(self.ontospy_graph.properties)
        s_total = len(self.ontospy_graph.skosConcepts)


        if False:
            # testing how a single tree would look like
            JSON_DATA_CLASSES = json.dumps(
            {'children' :
                [ {'children' : c_mylist, 'name' : 'Classes', 'id' : "classes" },
                {'children' : p_mylist, 'name' : 'Properties', 'id' : "properties" },
                {'children' : s_mylist, 'name' : 'Concepts', 'id' : "concepts" }],
                'name' : 'Entities', 'id' : "root"
                }
                )

        # hack to make sure that we have a default top level object
        JSON_DATA_CLASSES = json.dumps({'children' : c_mylist, 'name' : 'owl:Thing', 'id' : "None" })
        JSON_DATA_PROPERTIES = json.dumps({'children' : p_mylist, 'name' : 'Properties', 'id' : "None" })
        JSON_DATA_CONCEPTS = json.dumps({'children' : s_mylist, 'name' : 'Concepts', 'id' : "None" })

        extra_context = {
                        "ontograph": self.ontospy_graph,
    					"TOTAL_CLASSES": c_total,
    					"TOTAL_PROPERTIES": p_total,
    					"TOTAL_CONCEPTS": s_total,
    					'JSON_DATA_CLASSES' : JSON_DATA_CLASSES,
    					'JSON_DATA_PROPERTIES' : JSON_DATA_PROPERTIES,
    					'JSON_DATA_CONCEPTS' : JSON_DATA_CONCEPTS,
                        "theme": self.theme
                        }

        contents = self._renderTemplate("html-multi/d3tree.html", extraContext=extra_context)
        FILE_NAME = "entities-tree-view.html"
        self._save2File(contents, FILE_NAME, browser_output_path)

        if self.ontospy_graph.classes:
            # BROWSER PAGES - CLASSES ======
            for entity in self.ontospy_graph.classes:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "class",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_classinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.properties:
            # BROWSER PAGES - PROPERTIES ======

            for entity in self.ontospy_graph.properties:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "property",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_propinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        if self.ontospy_graph.skosConcepts:
            # BROWSER PAGES - CONCEPTS ======

            for entity in self.ontospy_graph.skosConcepts:
                extra_context = {"main_entity": entity,
                                "main_entity_type": "concept",
                                "theme": self.theme,
                                "ontograph": self.ontospy_graph
                                }
                extra_context.update(self.highlight_code(entity))
                contents = self._renderTemplate("html-multi/browser/browser_conceptinfo.html", extraContext=extra_context)
                FILE_NAME = entity.slug + ".html"
                self._save2File(contents, FILE_NAME, browser_output_path)


        return main_url




class KompleteVizMultiModel(KompleteViz):
    """
    Specialized version that supports customizing where the static url / folder are.

    The idea is to pass a location which can be shared by multiple html outputs. (eg multiple html-complex ontology folders)

    eg

    python -m ontospy.viz.scripts.export_all -o ~/Desktop/test2/ --theme random
    """


    def __init__(self, ontospy_graph, title="", theme="", static_url="", output_path_static=""):
        """
        Init
        """
        super(KompleteVizMultiModel, self).__init__(ontospy_graph, title, theme)
        self.static_files = ["custom", "libs"]
        self.theme = validate_theme(theme)
        self.static_url = static_url  # eg "../static"
        self.output_path_static = output_path_static  # eg full path to a top level
        # note: the following serves to make sure self.static_url is passed correctly
        self.basic_context_data = self._build_basic_context()






# if called directly, for testing purposes pick a random ontology

if __name__ == '__main__':

    TEST_ONLINE = False
    try:

        g = get_onto_for_testing(TEST_ONLINE)

        v = KompleteViz(g, title="", theme=random_theme())
        v.build()
        v.preview()

        sys.exit(0)

    except KeyboardInterrupt as e:  # Ctrl-C
        raise e
