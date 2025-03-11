import BlumBlumShub
import Tests

blum = BlumBlumShub.BlumBlumShub()
bits = blum.generate()
tests = Tests.Tests(bits)
tests.runTests()
