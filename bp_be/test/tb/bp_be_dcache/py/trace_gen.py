#
#   trace_gen.py
#


class TraceGen:

  # constructor
  def __init__(self, addr_width_p, data_width_p):
    self.addr_width_p = addr_width_p
    self.data_width_p = data_width_p
    self.packet_len = addr_width_p + data_width_p + 4 + 4

  # print header
  def print_header(self):
    print("#### generated by trace_gen.py ####")
    print("#### packet_len = " + str(self.packet_len) + " ####")
  
  # send load
  # signed: sign extend or not
  # size: load size in bytes
  # addr: load address
  def send_load(self, signed, size, addr):
    packet = "0001_"
    if (size == 8):
      packet += "0011_"
    else:
      if (signed):
        if (size == 1):
          packet += "0000_"
        elif (size == 2):
          packet += "0001_"
        elif (size == 4):
          packet += "0010_"
        else:
          raise ValueError("unexpected size for signed load.")
      else:
        if (size == 1):
          packet += "0100_"
        elif (size == 2):
          packet += "0101_"
        elif (size == 4):
          packet += "0110_"
        else:
          raise ValueError("unexpected size for unsigned load.")

    packet += format(addr, "0"+str(self.addr_width_p)+"b") + "_"
    packet += format(0, "064b")  
    print(packet)


  # send store
  # signed: sign extend or not
  # size: store size in bytes
  # addr: store address
  def send_store(self, size, addr, data):
    packet = "0001_"
    if (size == 1):
      packet += "1000_"
    elif (size == 2):
      packet += "1001_"
    elif (size == 4):
      packet += "1010_"
    elif (size == 8):
      packet += "1011_"
    else:
      raise ValueError("unexpected size for store.")
    packet += format(addr, "0" + str(self.addr_width_p) + "b") + "_"
    packet += format(data, "064b")
    print(packet)

  # receive data
  # data: expected data
  def recv_data(self, data):
    packet = "0010_0000_"
    packet += (self.addr_width_p)*"0" + "_" + format(data, "064b")
    print(packet)

  # wait for a number of cycles
  # num_cycles: number of cycles to wait.
  def wait(self, num_cycles):
    print("0110_" + format(num_cycles, "0" + str(self.packet_len-4) + "b"))
    print("0101_" + (self.packet_len-4)*"0")

  # finish trace
  def test_finish(self):
    print("#### FINISH ####")
    self.wait(8)
    print("0100_" + (self.packet_len-4)*"0")
 
  def test_done(self):
    print("#### DONE ####")
    self.wait(8)
    print("0011_" + (self.packet_len-4)*"0")

  # wait for a single cycle
  def nop(self):
    print("0000_" + "0"*(self.packet_len-4))
