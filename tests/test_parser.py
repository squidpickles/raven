# TODO
from raven.parser import RavenMessageParser, RavenCommand

def test_demand():
	msg = b'<InstantaneousDemand>\r\n  <DeviceMacId>0x00158d00001ab777</DeviceMacId>\r\n  <MeterMacId>0x0013500100d8c028</MeterMacId>\r\n  <TimeStamp>0x1cc0c525</TimeStamp>\r\n  <Demand>0x0004d2</Demand>\r\n  <Multiplier>0x00000001</Multiplier>\r\n  <Divisor>0x000003e8</Divisor>\r\n  <DigitsRight>0x03</DigitsRight>\r\n  <DigitsLeft>0x0f</DigitsLeft>\r\n  <SuppressLeadingZero>Y</SuppressLeadingZero>\r\n</InstantaneousDemand>\r\n'
	m = RavenMessageParser.parse(msg)
	assert m.calculate_number('Demand') == 1.234

def test_summation():
	msg = b'<CurrentSummationDelivered>\r\n  <DeviceMacId>0x00158d00001ab777</DeviceMacId>\r\n  <MeterMacId>0x0013500100d8c028</MeterMacId>\r\n  <TimeStamp>0x1cc0c215</TimeStamp>\r\n  <SummationDelivered>0x00000000021c17e2</SummationDelivered>\r\n  <SummationReceived>0x0000000000000000</SummationReceived>\r\n  <Multiplier>0x00000001</Multiplier>\r\n  <Divisor>0x000003e8</Divisor>\r\n  <DigitsRight>0x03</DigitsRight>\r\n  <DigitsLeft>0x0f</DigitsLeft>\r\n  <SuppressLeadingZero>Y</SuppressLeadingZero>\r\n</CurrentSummationDelivered>\r\n'
	m = RavenMessageParser.parse(msg)
	assert m.calculate_number('SummationDelivered') == 35395.554
