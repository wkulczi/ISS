import numpy as np
import skfuzzy
import skfuzzy.control as ctrl


class FuzzyLogic:
    def __init__(self):
        self.error: ctrl.Antecedent = None
        self.delta: ctrl.Antecedent = None
        self.universe = None
        self.output: ctrl.Consequent = None
        self.system: ctrl.ControlSystem = None
        self.simulation: ctrl.ControlSystemSimulation = None
        self.last_set_point = 0
        self.init_fuzzy_system()

    def init_fuzzy_system(self):
        universe = np.linspace(-10, 10, 9)
        self.error = ctrl.Antecedent(universe, 'error')
        self.delta = ctrl.Antecedent(universe, 'delta')
        self.output = ctrl.Consequent(universe, 'output')

        names = ['bdu', 'du', 'su', 'mu', 'z', 'md', 'sd', 'dd', 'bdd']

        self.error.automf(names=names)
        self.delta.automf(names=names)
        self.output.automf(names=names)

        rules = self.define_fuzzy_rules()
        self.system = ctrl.ControlSystem(rules=rules)
        self.simulation = ctrl.ControlSystemSimulation(self.system)

    def calculate(self, en, en_delta):
        self.simulation.input['error'] = en
        self.simulation.input['delta'] = en_delta
        self.simulation.compute()
        return self.simulation.output['output']

    def define_fuzzy_rules(self) -> object:
        #-4
        rule0 = ctrl.Rule(antecedent=((self.error['du'] & self.delta['du']) |
                                      (self.error['du'] & self.delta['su']) |
                                      (self.error['du'] & self.delta['mu']) |
                                      (self.error['su'] & self.delta['du']) |
                                      (self.error['su'] & self.delta['su']) |
                                      (self.error['mu'] & self.delta['du'])|
                                      (self.error['z'] & self.delta['bdu']) |
                                      (self.error['bdu'] & self.delta['z'])
                                      ),
                          consequent=self.output['bdu'], label='regula bdu')
        #-3
        rule1 = ctrl.Rule(antecedent=((self.error['z'] & self.delta['du']) |
                                      (self.error['mu'] & self.delta['su']) |
                                      (self.error['su'] & self.delta['mu']) |
                                      (self.error['du'] & self.delta['z']) |
                                      (self.error['bdu'] & self.delta['md']) |
                                      (self.error['md'] & self.delta['bdu'])),
                          consequent=self.output['du'], label='regula du')

        #-2
        rule2 = ctrl.Rule(antecedent=((self.error['md'] & self.delta['du']) |
                                      (self.error['z'] & self.delta['su']) |
                                      (self.error['mu'] & self.delta['mu']) |
                                      (self.error['su'] & self.delta['z']) |
                                      (self.error['du'] & self.delta['md'])|
                                      (self.error['bdu'] & self.delta['sd'])|
                                      (self.error['sd'] & self.delta['bdu'])),
                          consequent=self.output['su'], label='regula su')
        #-1
        rule3 = ctrl.Rule(antecedent=((self.error['sd'] & self.delta['du']) |
                                      (self.error['md'] & self.delta['su']) |
                                      (self.error['z'] & self.delta['mu']) |
                                      (self.error['mu'] & self.delta['z']) |
                                      (self.error['su'] & self.delta['md']) |
                                      (self.error['du'] & self.delta['sd'])|
                                      (self.error['bdu'] & self.delta['dd']) |
                                      (self.error['dd'] & self.delta['bdu'])
                                      ),
                          consequent=self.output['mu'], label='regula mu')
        #0
        rule4 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['du']) |
                                      (self.error['sd'] & self.delta['su']) |
                                      (self.error['md'] & self.delta['mu']) |
                                      (self.error['z'] & self.delta['z']) |
                                      (self.error['mu'] & self.delta['md']) |
                                      (self.error['su'] & self.delta['sd']) |
                                      (self.error['du'] & self.delta['dd'])|
                                      (self.error['bdu'] & self.delta['bdd']) |
                                      (self.error['bdd'] & self.delta['bdu'])
                                      ),
                          consequent=self.output['z'], label='regula z')
        #1
        rule5 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['su']) |
                                      (self.error['sd'] & self.delta['mu']) |
                                      (self.error['md'] & self.delta['z']) |
                                      (self.error['z'] & self.delta['md']) |
                                      (self.error['mu'] & self.delta['sd']) |
                                      (self.error['su'] & self.delta['dd'])|
                                      (self.error['du'] & self.delta['bdd']) |
                                      (self.error['bdd'] & self.delta['du'])
                                      ),
                          consequent=self.output['md'], label='regula md')
        #2
        rule6 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['mu']) |
                                      (self.error['sd'] & self.delta['z']) |
                                      (self.error['md'] & self.delta['md']) |
                                      (self.error['z'] & self.delta['sd']) |
                                      (self.error['mu'] & self.delta['dd'])|
                                      (self.error['su'] & self.delta['bdd']) |
                                      (self.error['bdd'] & self.delta['su'])
                                      ),
                          consequent=self.output['sd'], label='regula sd')
        #3
        rule7 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['z']) |
                                      (self.error['sd'] & self.delta['md']) |
                                      (self.error['md'] & self.delta['sd']) |
                                      (self.error['z'] & self.delta['dd'])|
                                      (self.error['du'] & self.delta['bdd']) |
                                      (self.error['bdd'] & self.delta['du'])
                                      ),
                          consequent=self.output['dd'], label='regula dd')
        #4
        rule8 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['md']) |
                                      (self.error['dd'] & self.delta['sd']) |
                                      (self.error['dd'] & self.delta['dd']) |
                                      (self.error['sd'] & self.delta['sd']) |
                                      (self.error['sd'] & self.delta['dd']) |
                                      (self.error['md'] & self.delta['dd']) |
                                      (self.error['z'] & self.delta['bdd']) |
                                      (self.error['bdd'] & self.delta['z'])
                                      ),
                          consequent=self.output['bdd'], label='regula bdd')
        return [rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
