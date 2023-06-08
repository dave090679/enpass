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
_taborder = list()
_tabindex = 0
class EnpassListItem(ListItem):
	def _get_name(self):
		l = list()
		for x in self.children:
			if x.role == controlTypes.Role.STATICTEXT:
				l.append(x.name)
		return "\t".join(l)

class EnpassTab(UIA):
	@script (
		gestures=["kb:space", "kb:enter"],
		description=_("switches to the selected Tab in enpass"),
		category=_("enpass")
		)
	def script_activatetab(self, gesture):
		gesture.send()
		api.getForegroundObject().children[1].firstChild.children[1].firstChild.firstChild.children[1].setFocus()
class AppModule(appModuleHandler.AppModule):
	def event_NVDAObject_init(self, obj):
		obj.shouldAllowIAccessibleFocusEvent = True
		if obj.name == "" and obj.childCount == 1 and obj.firstChild.name != "":
			obj.name = obj.firstChild.name


	@script (
		gesture="kb:F10",
		description=_("activates the menubar"),
		category=_("enpass")
		)
	def script_clickmenubar(self, gesture):
		api.getForegroundObject().children[1].firstChild.firstChild.firstChild.setFocus()

	@script (
		gesture="kb:F6",
		description=_("activates the settings tab bar"),
		category=_("enpass"))
	def script_clicktabs(self, gesture):
		try:
			api.getForegroundObject().children[1].firstChild.children[1].children[1].setFocus()
		except:
			pass


	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		if obj.role == controlTypes.Role.LISTITEM:
			clsList.insert(0,EnpassListItem)
		elif obj.role == controlTypes.Role.TAB and controlTypes.State.CHECKABLE in obj.states:
			clsList.insert(0,EnpassTab)
