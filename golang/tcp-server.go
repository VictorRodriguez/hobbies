package main

import "net"
import "fmt"
import "bufio"
import "strings" // only needed below for sample processing

func handleConnection(c net.Conn) {
	fmt.Printf("Serving %s\n", c.RemoteAddr().String())
	for {

		netData, err := bufio.NewReader(c).ReadString('\n')
		if err != nil {
			fmt.Println(err)
			return
		}

		temp := strings.TrimSpace(string(netData))
		if temp == "STOP" {
			break
		}

		// output message received
		fmt.Print("Message Received:", string(netData))
		// sample process for string received
		newmessage := strings.ToUpper(netData)
		// send new string back to client
		c.Write([]byte(newmessage + "\n"))
	}
	c.Close()
}

func main() {

	fmt.Println("Launching server...")

	// listen on all interfaces
	ln, err := net.Listen("tcp", ":8081")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer ln.Close()

	for {
		conn, err := ln.Accept()
		if err != nil {
			fmt.Println(err)
			return
		}
		go handleConnection(conn)

	}
}
