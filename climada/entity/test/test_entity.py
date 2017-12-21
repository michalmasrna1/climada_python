"""
=====================
test_entity module
=====================

Test Entity class.
"""
# Author: Gabriela Aznar Siguan (gabriela.aznar@usys.ethz.ch)
# Created on Fri Dec  8 14:52:28 2017

#    Copyright (C) 2017 by
#    David N. Bresch, david.bresch@gmail.com
#    Gabriela Aznar Siguan (g.aznar.siguan@gmail.com)
#    All rights reserved.

import unittest

from climada.entity.entity import Entity
from climada.entity.measures.source_excel import MeasuresExcel
from climada.entity.exposures.source_excel import ExposuresExcel
from climada.entity.exposures.base import Exposures
from climada.entity.discounts.base import Discounts
from climada.entity.impact_funcs.base import ImpactFuncs
from climada.entity.measures.base import Measures
from climada.util.constants import ENT_DEMO_XLS

class TestReader(unittest.TestCase):
    """Test reader functionality of the Entity class"""

    def test_default_pass(self):
        """Instantiating the Entity class the default entity file is loaded"""
        # Instance entity
        # Set demo file as default
        Entity.def_file = ENT_DEMO_XLS
        def_entity = Entity()

        # Check default demo excel file has been loaded
        self.assertEqual(len(def_entity.exposures.deductible), 50)
        self.assertEqual(def_entity.exposures.value[2], 12596064143.542929)

        self.assertEqual(len(def_entity.impact_funcs.data['TC'][1].mdd), 9)

        self.assertEqual(def_entity.measures.data[0].name, 'Mangroves')

        self.assertEqual(def_entity.discounts.years[5], 2005)

        self.assertTrue(isinstance(def_entity.discounts, Discounts))
        self.assertTrue(isinstance(def_entity.exposures, Exposures))
        self.assertTrue(isinstance(def_entity.impact_funcs, ImpactFuncs))
        self.assertTrue(isinstance(def_entity.measures, Measures))

    def test_wrong_input_fail(self):
        """ValueError is raised when a wrong input is provided"""
        # Instance entity
        exposures = MeasuresExcel
        impact_funcs = MeasuresExcel
        discounts = MeasuresExcel
        measures = ExposuresExcel
        
        # Set demo file as default
        Entity.def_file = ENT_DEMO_XLS

        with self.assertRaises(ValueError) as error:
            Entity(exposures=exposures)
            self.assertTrue('Exposures' in error.msg)

        with self.assertRaises(ValueError) as error:
            Entity(impact_funcs=impact_funcs)
            self.assertTrue('ImpactFuncs' in error.msg)

        with self.assertRaises(ValueError) as error:
            Entity(discounts=discounts)
            self.assertTrue('Discounts' in error.msg)

        with self.assertRaises(ValueError) as error:
            Entity(measures=measures)
            self.assertTrue('Measures' in error.msg)

        with self.assertRaises(ValueError) as error:
            ent = Entity()
            ent.discounts = ExposuresExcel
            self.assertTrue('Discounts' in error.msg)

# Execute TestReader
suite_reader = unittest.TestLoader().loadTestsFromTestCase(TestReader)
unittest.TextTestRunner(verbosity=2).run(suite_reader)
