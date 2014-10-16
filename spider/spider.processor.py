## Copyright (C) LIMSI-CNRS (2014)
##
## contributor(s) : Jorge Gascon, Damien Touraine, David Poirier-Quinot,
## Laurent Pointal, Julian Adenauer, 
## 
## This software is a computer program whose purpose is to distribute
## blender to render on Virtual Reality device systems.
## 
## This software is governed by the CeCILL  license under French law and
## abiding by the rules of distribution of free software.  You can  use, 
## modify and/ or redistribute the software under the terms of the CeCILL
## license as circulated by CEA, CNRS and INRIA at the following URL
## "http://www.cecill.info". 
## 
## As a counterpart to the access to the source code and  rights to copy,
## modify and redistribute granted by the license, users are provided only
## with a limited warranty  and the software's author,  the holder of the
## economic rights,  and the successive licensors  have only  limited
## liability. 
## 
## In this respect, the user's attention is drawn to the risks associated
## with loading,  using,  modifying and/or developing or reproducing the
## software by the user in light of its specific status of free software,
## that may mean  that it is complicated to manipulate,  and  that  also
## therefore means  that it is reserved for developers  and  experienced
## professionals having in-depth computer knowledge. Users are therefore
## encouraged to load and test the software's suitability as regards their
## requirements in conditions enabling the security of their systems and/or 
## data to be ensured and,  more generally, to use and operate it in the 
## same conditions as regards security. 
## 
## The fact that you are presently reading this means that you have had
## knowledge of the CeCILL license and that you accept its terms.
## 

import blendervr
import os

blendervr.processor.appendProcessor(os.path.join(blenderVR_root, 'samples', 'processors.py'))

if blendervr.is_virtual_environment():
    import bge

    class Processor(blendervr.processor.getProcessor()):
        def __init__(self, parent):
            super(Processor, self).__init__(parent, head_navigator = True)
            self._quit = 0
            self._controller = bge.logic.getCurrentController()

            if self.blenderVR.isMaster():
                self.blenderVR.getSceneSynchronizer().getItem(bge.logic).activate(True, True)
                self._navigator.setPositionFactors(1, 20.0, 1.0)

        def rum_a(self, info):
            if info['channel'][1] < 0.2:
                self._controller.activate(self._controller.actuators['act_vor_Laufen'])
                self._controller.activate(self._controller.actuators['vor_renn'])
                self._controller.deactivate(self._controller.actuators['act_back_Laufen'])
                self._controller.deactivate(self._controller.actuators['Back_renn'])
            elif info['channel'][1] > 0.8:
                self._controller.activate(self._controller.actuators['act_back_Laufen'])
                self._controller.activate(self._controller.actuators['Back_renn'])
                self._controller.deactivate(self._controller.actuators['act_vor_Laufen'])
                self._controller.deactivate(self._controller.actuators['vor_renn'])
            else:
                self._controller.deactivate(self._controller.actuators['act_back_Laufen'])
                self._controller.deactivate(self._controller.actuators['Back_renn'])
                self._controller.deactivate(self._controller.actuators['act_vor_Laufen'])
                self._controller.deactivate(self._controller.actuators['vor_renn'])

            if info['channel'][0] < 0.2:
                self._controller.activate(self._controller.actuators['act_Laufen_rechts'])
                self._controller.activate(self._controller.actuators['Laufen_Rechts'])
                self._controller.deactivate(self._controller.actuators['act_Laufen_links'])
                self._controller.deactivate(self._controller.actuators['Laufen_Links'])
            elif info['channel'][0] > 0.8:
                self._controller.activate(self._controller.actuators['act_Laufen_links'])
                self._controller.activate(self._controller.actuators['Laufen_Links'])
                self._controller.deactivate(self._controller.actuators['act_Laufen_rechts'])
                self._controller.deactivate(self._controller.actuators['Laufen_Rechts'])
            else:
                self._controller.deactivate(self._controller.actuators['act_Laufen_links'])
                self._controller.deactivate(self._controller.actuators['Laufen_Links'])
                self._controller.deactivate(self._controller.actuators['act_Laufen_rechts'])
                self._controller.deactivate(self._controller.actuators['Laufen_Rechts'])

        def rum_b(self, info):
            if (info['button'] == 26) and (info['state'] == 1):
                self._controller.activate(self._controller.actuators['act_Attack'])
            if (info['button'] == 23) and (info['state'] == 1):
                self._controller.activate(self._controller.actuators['Jump'])

else: # not VR screen => Console

    class Processor(blendervr.processor.getProcessor()):

        def __init__(self, console):
            super(Processor, self).__init__(console, ('designer', 'spider.ui'), head_navigator=True)

            if hasattr(self, '_navigator'):
                self._navigator.registerWidget(self._ui.HC_Nav)