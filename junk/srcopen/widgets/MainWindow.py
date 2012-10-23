# -*- coding:utf-8 -*-
# Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

"""
openFisca, Logiciel libre de simulation du système socio-fiscal français
Copyright © 2011 Clément Schaff, Mahdi Ben Jelloul

This file is part of openFisca.

    openFisca is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    openFisca is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with openFisca.  If not, see <http://www.gnu.org/licenses/>.
"""

import platform
from PyQt4.QtCore import (SIGNAL, SLOT, Qt, QSettings, QVariant, QSize, QPoint, 
                          PYQT_VERSION_STR, QT_VERSION_STR, QLocale)
from PyQt4.QtGui import (QMainWindow, QWidget, QGridLayout, QMessageBox, QKeySequence,
                         QApplication, QCursor, QPixmap, QSplashScreen, QColor,
                         QActionGroup, QStatusBar)

from Config import CONF, VERSION, ConfigDialog, SimConfigPage, PathConfigPage, CalConfigPage
from widgets.Parametres import ParamWidget
from widgets.Composition import ScenarioWidget
from widgets.Output import Graph, OutTable
from widgets.AggregateOuput import AggregateOutputWidget
from widgets.Calibration import CalibrationWidget
from widgets.ExploreData import ExploreDataWidget
from france.data import InputTable
from france.model import ModelFrance
from core.datatable import DataTable, SystemSf
from core.utils import gen_output_data, gen_aggregate_output, Scenario
from core.qthelpers import create_action, add_actions, get_icon
import gc

class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.dirty = False
        self.isLoaded = False
        self.calibration_enabled = False
        self.aggregate_enabled = False

        self.setObjectName("MainWindow")
        self.resize(800, 600)
        self.setWindowTitle("OpenFisca")
        app_icon = get_icon('OpenFisca22.png')
        self.setWindowIcon(app_icon)
        self.setLocale(QLocale(QLocale.French, QLocale.France))
        self.setDockOptions(QMainWindow.AllowNestedDocks|QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)

        self.centralwidget = QWidget(self)
        self.gridLayout = QGridLayout(self.centralwidget)
        self.setCentralWidget(self.centralwidget)
        self.centralwidget.hide()

        self.statusbar = QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        # Showing splash screen
        pixmap = QPixmap(':/images/splash.png', 'png')
        self.splash = QSplashScreen(pixmap)
        font = self.splash.font()
        font.setPixelSize(10)
        self.splash.setFont(font)
        self.splash.show()
        self.splash.showMessage("Initialisation...", Qt.AlignBottom | Qt.AlignCenter | 
                                Qt.AlignAbsolute, QColor(Qt.black))
#        if CONF.get('main', 'current_version', '') != __version__:
#            CONF.set('main', 'current_version', __version__)
            # Execute here the actions to be performed only once after
            # each update (there is nothing there for now, but it could 
            # be useful some day...
        
        self.scenario = Scenario()
        # Preferences
        self.general_prefs = [SimConfigPage, PathConfigPage, CalConfigPage]
        self.oldXAXIS = 'sal'
        self.reforme = False
        self.apply_settings()
        
        # Dockwidgets creation
        self.splash.showMessage("Creating widgets...", Qt.AlignBottom | Qt.AlignCenter | 
                                Qt.AlignAbsolute, QColor(Qt.black))

        self.create_dockwidgets()
        self.populate_mainwidow()

        #################################################################
        ## Menu initialization
        #################################################################
        self.splash.showMessage("Creating menubar...", Qt.AlignBottom | Qt.AlignCenter | 
                                Qt.AlignAbsolute, QColor(Qt.black))
        # Menu Fichier
        self.file_menu = self.menuBar().addMenu("Fichier")
        action_export_png = create_action(self, 'Exporter le graphique', icon = 'document-save png.png', triggered = self._graph.save_figure)
        action_export_csv = create_action(self, 'Exporter la table', icon = 'document-save csv.png', triggered = self._table.saveCsv)
        action_pref = create_action(self, u'Préférences', QKeySequence.Preferences, icon = 'preferences-desktop.png', triggered = self.edit_preferences)
        action_quit = create_action(self, 'Quitter', QKeySequence.Quit, icon = 'process-stop.png',  triggered = SLOT('close()'))
        
        file_actions = [action_export_png, action_export_csv,None, action_pref, None, action_quit]
        add_actions(self.file_menu, file_actions)

        # Menu Edit
        self.edit_menu = self.menuBar().addMenu(u"Édition")
        action_copy = create_action(self, 'Copier', QKeySequence.Copy, triggered = self.global_callback, data = 'copy')
        
        edit_actions = [None, action_copy]
        add_actions(self.edit_menu, edit_actions)

        # Menu Simulation
        self.simulation_menu = self.menuBar().addMenu(u"Simulation")

        self.action_refresh_bareme      = create_action(self, u'Calculer barèmes', shortcut = 'F9', icon = 'calculator_green.png', triggered = self.refresh_bareme)
        self.action_refresh_aggregate   = create_action(self, u'Calculer aggrégats', shortcut = 'F10', icon = 'calculator_blue.png', triggered = self.refresh_aggregate)

        self.action_calibrate = create_action(self, u'Caler les poids', shortcut = 'CTRL+K', icon = 'scale22.png', triggered = self.calibrate)

        action_bareme = create_action(self, u'Barème', icon = 'bareme22.png', toggled = self.modeBareme)
        action_cas_type = create_action(self, u'Cas type', icon = 'castype22.png', toggled = self.modeCasType)
        action_mode_reforme = create_action(self, u'Réforme', icon = 'comparison22.png', toggled = self.modeReforme, tip = u"Différence entre la situation simulée et la situation actuelle")
        mode_group = QActionGroup(self)
        mode_group.addAction(action_bareme)
        mode_group.addAction(action_cas_type)
        self.mode = 'bareme'
        action_bareme.trigger()

        simulation_actions = [self.action_refresh_bareme, self.action_refresh_aggregate , None, self.action_calibrate, None, action_bareme, action_cas_type, None, action_mode_reforme]
        add_actions(self.simulation_menu, simulation_actions)
        
        # Menu Help
        help_menu = self.menuBar().addMenu("&Aide")
        action_about = create_action(self, u"&About OpenFisca", triggered = self.helpAbout)
        action_help = create_action(self, "&Aide", QKeySequence.HelpContents, triggered = self.helpHelp)
        help_actions = [action_about, action_help]
        add_actions(help_menu, help_actions)
                
        # Display Menu
        view_menu = self.createPopupMenu()
        view_menu.setTitle("&Affichage")
        self.menuBar().insertMenu(help_menu.menuAction(),
                                  view_menu)
        
        # Toolbar
        self.main_toolbar = self.create_toolbar(u"Barre d'outil", 'main_toolbar')
        toolbar_actions = [action_export_png, action_export_csv, None, self.action_refresh_bareme,
                           self.action_refresh_aggregate, None, self.action_calibrate, None,
                            action_bareme, action_cas_type, None, action_mode_reforme]
        add_actions(self.main_toolbar, toolbar_actions)


        self.connect(self._menage,     SIGNAL('changed()'), self.changed_bareme)
        self.connect(self._parametres, SIGNAL('changed()'), self.changed_param)
        self.connect(self._aggregate_output, SIGNAL('calculated()'), self.calculated)
        self.connect(self, SIGNAL('weights_changed()'), self.refresh_aggregate)
        self.connect(self, SIGNAL('bareme_only()'), self.switch_bareme_only)
        
        # Window settings
        self.splash.showMessage("Restoring settings...", Qt.AlignBottom | Qt.AlignCenter | 
                                Qt.AlignAbsolute, QColor(Qt.black))
        settings = QSettings()
        size = settings.value('MainWindow/Size', QVariant(QSize(800,600))).toSize()
        self.resize(size)
        position = settings.value('MainWindow/Position', QVariant(QPoint(0,0))).toPoint()
        self.move(position)
        self.restoreState(settings.value("MainWindow/State").toByteArray())



        self.splash.showMessage("Loading survey data...", Qt.AlignBottom | Qt.AlignCenter | 
                                Qt.AlignAbsolute, QColor(Qt.black))
        
        self.enable_aggregate(True)
        
        self.refresh_bareme()
        
        self.isLoaded = True
        self.splash.hide()

    def create_toolbar(self, title, object_name, iconsize=24):
        toolbar = self.addToolBar(title)
        toolbar.setObjectName(object_name)
        toolbar.setIconSize( QSize(iconsize, iconsize) )
        return toolbar

    def create_dockwidgets(self):
        # Création des dockwidgets
        self._parametres = ParamWidget('data/param.xml', self)
        self._menage = ScenarioWidget(self.scenario, self)
        self._graph = Graph(self)
        self._table = OutTable(self)
        self._aggregate_output = AggregateOutputWidget(self)
        self._dataframe_widget = ExploreDataWidget(self)
        
    def populate_mainwidow(self):
        '''
        Creates all dockwidgets
        '''
        self.addDockWidget(Qt.RightDockWidgetArea, self._parametres)
        self.addDockWidget(Qt.RightDockWidgetArea, self._menage)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._graph)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._table)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._aggregate_output)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._dataframe_widget)
        self.tabifyDockWidget(self._dataframe_widget, self._aggregate_output)
        self.tabifyDockWidget(self._aggregate_output, self._table)
        self.tabifyDockWidget(self._table, self._graph)
        
    def global_callback(self):
        """Global callback"""
        widget = QApplication.focusWidget()
        action = self.sender()
        callback = unicode(action.data().toString())
        if hasattr(widget, callback):
            getattr(widget, callback)()

    def load_survey_data(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        try:
            # liberate some memory before loading new data
            self.reset_aggregate()
            gc.collect()
            fname = CONF.get('paths', 'survey_data/file')
            self.survey = DataTable(InputTable, survey_data = fname)
            self._dataframe_widget.set_dataframe(self.survey.table)
            return True
        except Exception, e:
            self.aggregate_enabled = False
            QMessageBox.warning(self, u"Impossible de lire les données", 
                                u"OpenFisca n'a pas réussi à lire les données d'enquête et passe en mode barème. L'erreur suivante a été renvoyé:\n%s\n\nVous pouvez charger des nouvelles données d'enquête dans Fichier>Paramètres>Chemins>Données d'enquête"%e)
            self.emit(SIGNAL('baremeOnly()'))
            return False
        finally:
            QApplication.restoreOverrideCursor()
        
    def enable_aggregate(self, val = True):
        survey_enabled = CONF.get('paths', 'survey_data/survey_enabled')
        loaded = False
        if val and survey_enabled:
            loaded = self.load_survey_data()

        if loaded:
            # Show widgets and enabled actions
            self.aggregate_enabled = True
            self._aggregate_output.setEnabled(True)
            self._aggregate_output.show()
            self._dataframe_widget.show()
            self.action_refresh_aggregate.setEnabled(True)
            self.action_calibrate.setEnabled(True)
        else:
            self.switch_bareme_only()

    def switch_bareme_only(self):
            self.aggregate_enabled = False
            self._aggregate_output.setEnabled(False)
            self._aggregate_output.hide()
            self._dataframe_widget.hide()
            self.action_refresh_aggregate.setEnabled(False)
            self.action_calibrate.setEnabled(False)

    def reset_aggregate(self):
        '''
        Clear all pointers to the survey data to allow its garbage collection
        '''
        self.survey = None
        self.survey_outputs = None
        self._dataframe_widget.clear()
        self._aggregate_output.clear()

    def calibrate(self):    
        # liberate some memory before loading new data
        calibration = CalibrationWidget(inputs = self.survey, outputs = self.survey_outputs, parent = self)
        calibration.exec_()
                
    def modeReforme(self, b):
        self.reforme = b
        self.changed_bareme()

    def modeBareme(self):
        self.mode = 'bareme'
        NMEN = CONF.get('simulation', 'nmen')
        if NMEN == 1: CONF.set('simulation', 'nmen', 101)
        self.changed_bareme()

    def modeCasType(self):
        self.mode = 'castype'
        CONF.set('simulation', 'nmen', 1)
        self.changed_bareme()

    def refresh_bareme(self):
        # Consistency check on scenario
        msg = self.scenario.check_consistency()
        if msg:
            QMessageBox.critical(self, u"Ménage non valide",
                                 msg, 
                                 QMessageBox.Ok, QMessageBox.NoButton)
            return False
        # Si oui, on lance le calcul
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        self.statusbar.showMessage(u"Calcul en cours...")
        self.action_refresh_bareme.setEnabled(False)
        # set the table model to None before changing data
        self._table.clearModel()
        
        P_default = self._parametres.getParam(defaut = True)    
        P_courant = self._parametres.getParam(defaut = False)
        
        input_table = DataTable(InputTable, scenario = self.scenario)

        population_courant = SystemSf(ModelFrance, P_courant, P_default)
        population_courant.set_inputs(input_table)
        data_courant = gen_output_data(population_courant)

        if self.reforme:
            population_default = SystemSf(ModelFrance, P_default, P_default)
            population_default.set_inputs(input_table)
            data_default = gen_output_data(population_default)
            data_courant.difference(data_default)
        else:
            data_default = data_courant
        self._table.updateTable(data_courant, reforme = self.reforme, mode = self.mode, dataDefault = data_default)
        self._graph.updateGraph(data_courant, reforme = self.reforme, mode = self.mode, dataDefault = data_default)

        self.statusbar.showMessage(u"")
        QApplication.restoreOverrideCursor()
    
    def compute_aggregate(self):
        P_default = self._parametres.getParam(defaut = True)    
        P_courant = self._parametres.getParam(defaut = False)
        
        input_table = self.survey

        output_table = SystemSf(ModelFrance, P_courant, P_default)
        output_table.set_inputs(input_table)
        
        output_table.calculate()
        
        return output_table
    
    def refresh_aggregate(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        self.statusbar.showMessage(u"Calcul des aggrégats en cours, ceci peut prendre quelques minutes...")
        self.action_refresh_aggregate.setEnabled(False)

        self._aggregate_output.clear()
        self._dataframe_widget.clear()
        self.survey_outputs = None
        gc.collect()

        self.survey_outputs = self.compute_aggregate()

        self._dataframe_widget.set_dataframe(self.survey_outputs.table)
        data_courant = gen_aggregate_output(self.survey_outputs)
        self._aggregate_output.update_output(data_courant, self.survey.description)
        
        self.statusbar.showMessage(u"")
        QApplication.restoreOverrideCursor()
        
    
    def closeEvent(self, event):
        if self.okToContinue():
            settings = QSettings()
            settings.setValue('MainWindow/Size', QVariant(self.size()))
            settings.setValue('MainWindow/Position', QVariant(self.pos()))
            settings.setValue('MainWindow/State', QVariant(self.saveState()))
        else:
            event.ignore()
    
    def okToContinue(self):
        if self.dirty:
            reply = QMessageBox.question(self, 
                                         "OpenFisca",
                                         "Voulez-vous quitter ?",
                                         QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.No:
                return False
        return True
    
    def helpAbout(self):
        QMessageBox.about(self, u"About OpenFisca",
                          u''' <b>OpenFisca</b><sup>beta</sup> v %s
                          <p> Copyright &copy; 2011 Clément Schaff, Mahdi Ben Jelloul
                          Tout droit réservé
                          <p> License GPL version 3 ou supérieure
                          <p> Python %s - Qt %s - PyQt %s on %s'''
                          % (VERSION, platform.python_version(),
                          QT_VERSION_STR, PYQT_VERSION_STR, platform.system()))

    def helpHelp(self):
        QMessageBox.about(self, u"Aide OpenFisca",
                          u'''<p> L'aide n'est pas disponible pour le moment. Pour plus
                          d'information, aller à <a href = www.openfisca.fr> www.openfisca.fr </a>
                          ''')

    def apply_settings(self):
        """Apply settings changed in 'Preferences' dialog box"""
        self.XAXIS = CONF.get('simulation', 'xaxis')
        if not self.XAXIS == self.oldXAXIS:
            self.scenario.indiv[0][self.oldXAXIS + 'i']=0
        if self.isLoaded == True:
            self._parametres.initialize()
            self.refresh_bareme()
        if self.calibration_enabled:
            self.action_calibrate.setEnabled(True)
        if self.aggregate_enabled:
            self.action_refresh_aggregate.setEnabled(True)

    def edit_preferences(self):
        """Edit OpenFisca preferences"""
        dlg = ConfigDialog(self)
        for PrefPageClass in self.general_prefs:
            widget = PrefPageClass(parent = dlg, main=self)
            widget.initialize()
            dlg.add_page(widget)

        dlg.show()
        dlg.check_all_settings()
        dlg.exec_()

    def changed_bareme(self):
        self.statusbar.showMessage(u"Appuyez sur F9 pour lancer la simulation")
        self.action_refresh_bareme.setEnabled(True)
    
    def changed_param(self):
        self.statusbar.showMessage(u"Appuyez sur F9/F10 pour lancer la simulation")
        if self.aggregate_enabled:
            self.action_refresh_aggregate.setEnabled(True)
                
        self.action_refresh_bareme.setEnabled(True)
            
    def calculated(self):
        self.statusbar.showMessage(u"Aggrégats calculés")
        self.emit(SIGNAL('aggregate_calculated()'))
        self.action_refresh_aggregate.setEnabled(False)
            
        