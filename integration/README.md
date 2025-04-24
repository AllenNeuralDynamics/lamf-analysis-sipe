Integration tests for expected calls to the executable produced by this
 respository. To closely match production environment, testing environment should:
 - be windows 10
 - using python==3.9.5

Batch files prefixed with `test-` are for testing different expected executable usage patterns. Some take a large amount of time/resources (~20min runtime, 10GB RAM). Files `not` prefixed with `test-` are just general utilities.
