#include<iostream>
#include<string.h>
using namespace std;

void sendDataTelemetry(string telemetry)
{

    return ;
}

string recieveDataTelemetry()
{
    // Recieve one packet
    return ;
}

void parsePacket( string packet )
{
    int len = strlen("packet");
    string comma = ",";
    size_t pos = 0;
    string data;
    string cmd;
    string id;
    string command;
    string commandMode;
    string arr[4];
    int i = 0;
    while ((pos = packet.find(comma)) != string::npos)
    {
        data = packet.substr(0, pos);
        if (i==0)
        {   
            if (data == "CMD") 
            {
                cmd = data;
            }
            else 
            {
                cmd = "***";
            }
        }
        if (i==1)

        {
            if (data == "1062")
            {
                id = "1062";
            
            }
            else 
            {
                id = "****";
            }
        }
        if (i==2)
        {
            command = data;
        }
        else
        {
            command = "*******";
        }
        packet.erase(0, pos + comma.length());
        i++;
       
    }
    if (packet == "")
    {
        commandMode = "****";
    }
    else
    {
        commandMode = packet;
    }
    arr[0] = cmd;
    arr[1] = id;
    arr[2] = command;
    arr[3] = commandMode;
        
    //Parse the packet and slit it into all the nessasary ints and floats 
}