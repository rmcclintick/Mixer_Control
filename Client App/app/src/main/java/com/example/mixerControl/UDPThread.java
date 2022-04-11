package com.example.mixerControl;

import java.io.IOException;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.net.SocketTimeoutException;

public class UDPThread extends Thread {
    private final static int PACKETSIZE = 100;
    private final static int JAVA_SERVER_PORT = 4445;
    private final static String PYTHON_SERVER_HOST = "192.168.1.197";
    private final static int PYTHON_SERVER_PORT = 4446;

    protected DatagramSocket rxsocket = null;
    protected DatagramSocket txsocket = null;
    protected InetAddress txhost = null;
    private volatile boolean StopServer = false;

    DatagramPacket packet = null;
    DatagramPacket lastPacket = null;
    private String IP;
    MainActivity ui;

    public UDPThread(String IP, MainActivity ui) throws IOException
    {
        this.IP = IP;
        this.ui = ui;
        rxsocket = new DatagramSocket(JAVA_SERVER_PORT);
        rxsocket.setSoTimeout(250);
        txhost = InetAddress.getByName(this.IP);
        txsocket = new DatagramSocket();
    }

    public void sendMessage(String message) throws IOException
    {
        byte[] data = message.getBytes();
        packet = new DatagramPacket(data, data.length, txhost, PYTHON_SERVER_PORT);
        //System.out.println("sendingMessage");
    }

    public String getIP()
    {
        return IP;
    }

    @Override
    public void run()
    {
        try {
            while (!StopServer) {
                //send only new packets
                if (packet != lastPacket)
                {
                    //System.out.println(packet);
                    txsocket.send(packet);
                    lastPacket = packet;
                }



                byte buf[] = new byte[PACKETSIZE];
                DatagramPacket packet = new DatagramPacket(buf, buf.length);
                try {
                    rxsocket.receive(packet);
                    String data = new String(packet.getData(), 0, packet.getLength());
                    //System.out.println(data);
                    if (data.startsWith("refresh"))
                    {
                        String[] names = data.split(" ");
                        String[] newNames = new String[names.length - 1];
                        for (int i = 1; i < names.length; i++)
                        {
                            newNames[i-1] = names[i];
                            System.out.println(names[i]);
                        }
                        System.out.println(newNames.length);

                        ui.runOnUiThread(new Runnable() {

                            @Override
                            public void run() {
                                ui.createFaders(newNames);
                            }
                        });

                    }

                } catch (SocketTimeoutException e) {
                }
            }
            rxsocket.close();
        } catch (IOException e) {
            System.out.println("IOException");
        }
    }
}
