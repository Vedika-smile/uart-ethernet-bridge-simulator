# UART to Ethernet Bridge Simulator

A software simulation of protocol translation between UART (serial) 
and TCP/IP (network), inspired by the core functionality of 
Network Interface Cards (NICs) in data center infrastructure.

## Motivation
Modern data center NICs (like NVIDIA ConnectX) perform hardware-level 
protocol translation between serial interfaces and high-speed networks. 
This project simulates that bridge in software — built on top of a 
previously designed UART transceiver in Verilog RTL.

## Architecture
