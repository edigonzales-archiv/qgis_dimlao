# Makefile for a PyQGIS plugin 
UI_FILES = Ui_dimensioning.py

RESOURCE_FILES = resources.py

PLUGINNAME = dimlao



default: compile
	
compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

dclean:
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname "*.pyc" -delete
	find $(HOME)/.qgis2/python/plugins/$(PLUGINNAME) -iname ".svn" -prune -exec rm -Rf {} \;

zip: dclean 
	rm -f $(PLUGINNAME).zip
	cd $(HOME)/.qgis2/python/plugins; zip -9r $(CURDIR)/$(PLUGINNAME).zip $(PLUGINNAME)
