GEDIT_PLUGIN_DIR = ~/.local/share/gedit/plugins

install:
	@if [ ! -d $(GEDIT_PLUGIN_DIR) ]; then \
		mkdir -p $(GEDIT_PLUGIN_DIR);\
	fi
	@echo "installing tabs_extend plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/tabs_extend*;
	@cp -R tabs_extend* $(GEDIT_PLUGIN_DIR);

uninstall:
	@echo "uninstalling tabs_extend plugin";
	@rm -rf $(GEDIT_PLUGIN_DIR)/tabs_extend*;
