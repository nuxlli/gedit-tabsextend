# -*- coding: utf-8 -*-
#
# Copyright © 2008, Éverton Ribeiro <nuxlli@gmail.com>
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#

import gtk
import gedit

# TODO: Open last close (Ctrl+Shit+t)
# TODO: Menu Close All (Ctrl+Shit+w)
# TODO: Menu Close Others (Ctrl+Shit+o)

# Find widget by name
def lookup_widget(base, widget_name):
  widgets = []

  for widget in base.get_children():
    if widget.get_name() == widget_name:
      widgets.append(widget)
    if isinstance(widget, gtk.Container):
      widgets += lookup_widget(widget, widget_name)

  return widgets

class TabsExtendWindowHelper:
  handler_ids = []

  def __init__(self, plugin, window):
    self.window   = window
    self.notebook = self.get_notebook()

    self.add_all()
    self.handler_ids.append((self.notebook, self.notebook.connect("tab_added", self.tab_added_handler)))
    self.handler_ids.append((self.notebook, self.notebook.connect("tab_removed", self.tab_removed_handler)))

  def deactivate(self):
    # disconnect
    for (handler_id, widget) in self.handler_ids:
      widget.disconnect(handler_id)

    self.window   = None
    self.notebook = None
    self.handles  = None

  def update_ui(self):
    pass

  def get_notebook(self):
    return lookup_widget(self.window, 'GeditNotebook')[0]

  def add_all(self):
    for x in range(self.notebook.get_n_pages()):
      tab = self.notebook.get_nth_page(x)
      self.add_middle_click_in_tab(tab)

  def add_middle_click_in_tab(self, tab):
    eventbox   = self.notebook.get_tab_label(tab).get_children()[0]
    handler_id = eventbox.connect("button-press-event", self.middle_click_handler, tab)
    self.handler_ids.append([eventbox, handler_id])

  def middle_click_handler(self, widget, event, tab):
    if event.type == gtk.gdk.BUTTON_PRESS and event.button == 2:
      if self.notebook.get_n_pages():
        self.notebook.prev_page()
      self.window.close_tab(tab)

  def tab_added_handler(self, widget, tab):
    self.add_middle_click_in_tab(tab)

  def tab_removed_handler(self, widget, tab):
    for (handler_id, widget) in self.handler_ids:
      if widget == tab:
        widget.disconnect(handler_id)
        self.handler_ids.remove(handler_id)
        break

class TabsExtendPlugin(gedit.Plugin):
    def __init__(self):
        gedit.Plugin.__init__(self)
        self._instances = {}

    def activate(self, window):
        self._instances[window] = TabsExtendWindowHelper(self, window)

    def deactivate(self, window):
        self._instances[window].deactivate()
        del self._instances[window]

    def update_ui(self, window):
        self._instances[window].update_ui()
