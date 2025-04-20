import QuantLib as ql

class PricingEngine:
    """
    Abstract base class for pricing engines.

    This class defines the interface for building QuantLib-compatible pricing engines.
    Subclasses must implement the `build` method to return a specific engine instance.
    
    Attributes:
        model_process: The QuantLib pricing model or process used for option pricing.
    """


    def __init__(self, model_process):
        """
        Initialize the base pricing engine.

        Args:
            model_process: The QuantLib model or process used by the engine.
        """

        self.model_process = model_process


    def build(self):
        raise NotImplementedError("Subclasses must implement this method.")


class BinomialEngine(PricingEngine):
    """
    Binomial tree pricing engine for vanilla options.

    This engine uses the Cox-Ross-Rubinstein (CRR) binomial method for pricing.
    
    Attributes:
        steps (int): Number of binomial steps used in the tree.
    """


    def __init__(
            self,
            model_process: ql.BlackScholesMertonProcess,
            steps=100
        ):
        """
        Initialize the binomial pricing engine.

        Args:
            model_process (ql.BlackScholesMertonProcess): The process to model the asset dynamics.
            steps (int, optional): Number of steps in the binomial tree. Default is 100.
        """

        super().__init__(model_process)
        self.steps = steps


    def build(self):
        """
        Build and return a binomial pricing engine using the CRR method.

        Returns:
            ql.BinomialVanillaEngine: The configured binomial pricing engine.
        """

        return ql.BinomialVanillaEngine(self.model_process, 'crr', self.steps)


class AnalyticEuropeanEngine(PricingEngine):
    """
    Analytic pricing engine for European options using the Black-Scholes model.
    """


    def __init__(
            self,
            model_process: ql.BlackScholesMertonProcess
        ):
        """
        Initialize the analytic European pricing engine.

        Args:
            model_process (ql.BlackScholesMertonProcess): The process modeling asset dynamics.
        """

        super().__init__(model_process)

    def build(self):
        """
        Build and return an analytic pricing engine for European options.

        Returns:
            ql.AnalyticEuropeanEngine: The analytic engine based on the Black-Scholes model.
        """

        return ql.AnalyticEuropeanEngine(self.model_process)


class HestonEngine(PricingEngine):
    """
    Pricing engine for options under the Heston stochastic volatility model.
    """


    def __init__(
            self,
            model_process: ql.HestonModel
        ):
        """
        Initialize the Heston pricing engine.

        Args:
            model_process (ql.HestonModel): The Heston model used to capture stochastic volatility.
        """

        super().__init__(model_process)

    def build(self):
        """
        Build and return an analytic Heston pricing engine.

        Returns:
            ql.AnalyticHestonEngine: The engine based on the analytic Heston model.
        """
        
        return ql.AnalyticHestonEngine(self.model_process)
