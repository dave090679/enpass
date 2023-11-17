#appModules/enpass.py
# Ein Teil von NonVisual Desktop Access (NVDA)
# Copyright (C) 2006-2023 NVDA Mitwirkende
# Diese Datei unterliegt der GNU General Public License.
# Weitere Informationen finden Sie in der Datei COPYING.
import appModuleHandler
import controlTypes
import api
from scriptHandler import script
import addonHandler
import mouseHandler
from NVDAObjects.UIA import ListItem, UIA
import tones
# Entfernen Sie das Kommentarzeichen (#) aus der nächsten Zeile, wenn (und sobald) die Datei zu einem Addon gehört. Dadurch werden Lokalisierungsfunktionen (Übersetzungsfunktionen) in Ihrer Datei aktiviert. Weitere Informationen finden Sie im Entwicklungshandbuch für NVDA-Addons.
addonHandler.initTranslation()
class EnpassEditableText(UIA):
	def _get_name(self):
		s = self.UIAElement.CurrentName
		try:
			s = self.previous.name
		except:
			pass
		return s
class EnpassListItem(ListItem):
	def _get_name(self):
		l = list()
		for x in self.children:
			if x.role == controlTypes.Role.STATICTEXT:
				l.append(x.name)
			elif x.role == controlTypes.Role.EDITABLETEXT:
				l.append(x.value)
		s = "\t".join(l)
		if s == "":
			s = self.UIAElement.CurrentName
		return s
class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		obj.shouldAllowIAccessibleFocusEvent = True
		if obj.name == "" and obj.childCount == 1 and obj.firstChild.name != "":
			obj.name = obj.firstChild.name
		if obj.role == controlTypes.Role.MENUBAR:
			if not hasattr(self, "_menubars"):
				self._menubars = list() 
			self._menubars.append(obj) 
		if obj.role == controlTypes.Role.TAB and controlTypes.State.CHECKED in obj.states:
			if not hasattr(self, "_tabcontrols"):
				self._tabcontrols = list() 
			self._tabcontrols.append(obj)
	@script (
		gesture="kb:F10",
		description=_("activates the menu bar"),
		category=_("enpass"))
	def script_clickmenubar(self, gesture):
		try:
			seelf._menubars[0].setFocus()
		except:
			pass

	@script (
		gesture="kb:F6",
		description=_("activates the settings tab bar"),
		category=_("enpass"))
	def script_clicktabs(self, gesture):
		try:
			seelf._tabcontrols[0].setFocus()
		except:
			pass

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.LISTITEM and isinstance(obj, UIA):
			clsList.insert(0,EnpassListItem)
		elif obj.role == controlTypes.Role.EDITABLETEXT and obj.name == "":
			clsList.insert(0,EnpassEditableText)
