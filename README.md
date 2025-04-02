# pytrade_bot
An approach to a modular, object-oriented trading bot, designed for automated financial market trading. This system leverages traditional indicators and machine learning models to analyze, predict, and execute trades across multiple assets.

## Implementation Abstract
This repo is designed to implement one instance of a bot that represents the potential work done by a trader. It contains macro- and micro-level analysis; for determining assets with potential profit and determining when, on a micro level, to buy/sell to maximise profit.

### 'Bots'
A trader bot is expected to handle micro-level understanding of a stock. A scouter bot will handle macro-level trend analysis of a stock. 

### 'Indicators'
Indicators are descriptive about the asset's data. They come in two forms, literal (LiteralIndicator) and series (SeriesIndicator). LiteralIndicator inheritence classes will return numeric values that represent some aspect of the data; noise, volatility. SeriesIndicator inheritence classes will return a Pandas Series object that has transformed some of the asset data into something else, that can be used for further analysis. SeriesIndicators can give us continuous-level analysis to indicate predictions, whereas LiteralIndicators are more likely to indicate confidence.

### 'Signals'
Signals are enumerators that hold simple values. For example, in the case of Trade signals: BUY, HOLD, SELL, SQUEEZE. These hold numeric representations: 1, 0, -1, 2. Squeeze is tempoprary, and represents an uncertain signal. 

### 'Strategies'
Strategies are the main mathematic implementation of Indicators. They can be fairly simple (BollingerStrategy) or complex (INSERT_HERE). They receive information from Indicators, and turn these indicator values into signals. Signals are enumerator objects that contain BUY, HOLD, SELL (and, at the moment, uncertainty signals like SQUEEZE). Signals will then be turned into a Confidence Index Vector (CIV), which represents the Strategy object's confidence in each of the three main signals; BUY, HOLD, SELL. It does this to convert indicator noise (as numerous indicators may give differing signals) into a numeric representation of confidence that can be used by bot decision-making.

### 'Machine Learning' 
Machine learning will, hopefully, be implemented to some degree. Early builds currently contain an ARIMA-EGARCH model for predicting ROI and assessing the variance of the residuals associated with that prediction. This can be implemented by a Strategy object to turn that prediction/variance pairing into Signals, then into a CIV. 

### 'Risk'
WIP

### 'Broker'
WIP
