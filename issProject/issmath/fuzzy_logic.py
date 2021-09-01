import numpy as np
import skfuzzy.control as ctrl


class FuzzyLogic:
    def __init__(self):
        self.error: ctrl.Antecedent = None
        self.delta: ctrl.Antecedent = None
        self.universe = None
        self.output: ctrl.Consequent = None
        self.system: ctrl.ControlSystem = None
        self.simulation: ctrl.ControlSystemSimulation = None
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

    def calculate(self, en, en_sum, en_delta):
        self.simulation.input['error'] = en
        self.simulation.input['delta'] = en_delta
        self.simulation.compute()
        return self.simulation.output['output']

# uchyb i zmiana uczybu to jedna baza reguł i wynik tego działania daje dla klolejnej bazy opis kolumny,czy wiersza i w ten sposób przez nawiasowanie można to sobie też
# żeby nie budować 3wymiarowej bazy reguł. takie dwustopniowe mapowanie
# uchyb = wartosc zadana - wartosc zmierzona / współczynnik jakis np jesli 10 to przestrzen numeryczna [-10,10].
# można zostawić 0,10, jak jest tereaz, ale wtedy 0-5 ma zamykac zawor 5-10 otweirac
# na razie korzystamy z bledu i roznicy z poprzednim. mamy pd, wystarczy sumowac i dostaniemy pi
# to co wyznaczy reg rozmyty nie jest sygnałem sterującym i nie z tego wyliczamy natezenie dopływu,
# tylko dodajemy to do wartosci poprzedniej i dopiero z tego wyznaczamy natezenie dopływu. i tak mamy regulator fuzzy pi
    def define_fuzzy_rules(self):
        rule0 = ctrl.Rule(antecedent=((self.error['du'] & self.delta['du']) |
                                      (self.error['du'] & self.delta['su']) |
                                      (self.error['du'] & self.delta['mu']) |
                                      (self.error['su'] & self.delta['du']) |
                                      (self.error['su'] & self.delta['su']) |
                                      (self.error['mu'] & self.delta['du'])),
                          consequent=self.output['bdu'], label='regula bdu')

        rule1 = ctrl.Rule(antecedent=((self.error['z'] & self.delta['du']) |
                                      (self.error['mu'] & self.delta['su']) |
                                      (self.error['su'] & self.delta['mu']) |
                                      (self.error['du'] & self.delta['z'])),
                          consequent=self.output['du'], label='regula du')

        rule2 = ctrl.Rule(antecedent=((self.error['md'] & self.delta['du']) |
                                      (self.error['z'] & self.delta['su']) |
                                      (self.error['mu'] & self.delta['mu']) |
                                      (self.error['su'] & self.delta['z']) |
                                      (self.error['du'] & self.delta['md'])),
                          consequent=self.output['su'], label='regula su')

        rule3 = ctrl.Rule(antecedent=((self.error['sd'] & self.delta['du']) |
                                      (self.error['md'] & self.delta['su']) |
                                      (self.error['z'] & self.delta['mu']) |
                                      (self.error['mu'] & self.delta['z']) |
                                      (self.error['su'] & self.delta['md']) |
                                      (self.error['du'] & self.delta['sd'])),
                          consequent=self.output['mu'], label='regula mu')

        rule4 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['du']) |
                                      (self.error['sd'] & self.delta['su']) |
                                      (self.error['md'] & self.delta['mu']) |
                                      (self.error['z'] & self.delta['z']) |
                                      (self.error['mu'] & self.delta['md']) |
                                      (self.error['su'] & self.delta['sd']) |
                                      (self.error['du'] & self.delta['dd'])),
                          consequent=self.output['z'], label='regula z')

        rule5 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['su']) |
                                      (self.error['sd'] & self.delta['mu']) |
                                      (self.error['md'] & self.delta['z']) |
                                      (self.error['z'] & self.delta['md']) |
                                      (self.error['mu'] & self.delta['sd']) |
                                      (self.error['su'] & self.delta['dd'])),
                          consequent=self.output['md'], label='regula md')

        rule6 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['mu']) |
                                      (self.error['sd'] & self.delta['z']) |
                                      (self.error['md'] & self.delta['md']) |
                                      (self.error['z'] & self.delta['sd']) |
                                      (self.error['mu'] & self.delta['dd'])),
                          consequent=self.output['sd'], label='regula sd')

        rule7 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['z']) |
                                      (self.error['sd'] & self.delta['md']) |
                                      (self.error['md'] & self.delta['sd']) |
                                      (self.error['z'] & self.delta['dd'])),
                          consequent=self.output['dd'], label='regula dd')

        rule8 = ctrl.Rule(antecedent=((self.error['dd'] & self.delta['md']) |
                                      (self.error['dd'] & self.delta['sd']) |
                                      (self.error['dd'] & self.delta['dd']) |
                                      (self.error['sd'] & self.delta['sd']) |
                                      (self.error['sd'] & self.delta['dd']) |
                                      (self.error['md'] & self.delta['dd'])),
                          consequent=self.output['bdd'], label='regula bdd')
        return [rule0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8]
