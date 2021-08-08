using System;
using System.CommandLine;
using System.CommandLine.Invocation;
using System.Management;

namespace SharpSCCM
{
    static class Program
    {
        static ManagementScope NewSccmConnection(string server, string sitecode)
        {
            ConnectionOptions connection = new ConnectionOptions();
            ManagementScope scope = new ManagementScope("\\\\" + server + "\\root\\SMS\\site_" + sitecode, connection);
            scope.Connect();
            return scope;
            /*
            catch (System.UnauthorizedAccessException unauthorizedErr)
            {
                Console.WriteLine("Connection error (user name or password might be incorrect): " + unauthorizedErr.Message);
                Environment.Exit(1);
            }
            */
        }

        static void FindLocalSccmInfo()
        {
            ConnectionOptions connection = new ConnectionOptions();
            ManagementScope scope = new ManagementScope("\\\\127.0.0.1\\root\\CCM", connection);
            scope.Connect();
            ObjectQuery query = new ObjectQuery("SELECT CurrentManagementPoint,Name FROM SMS_Authority");
            ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);

            Console.WriteLine("-----------------------------------");
            Console.WriteLine("SMS_Authority instance");
            Console.WriteLine("-----------------------------------");

            foreach (ManagementObject queryObj in searcher.Get())
            {
                foreach (PropertyData prop in queryObj.Properties)
                {
                    Console.WriteLine("{0}: {1}", prop.Name, prop.Value);
                }
                Console.WriteLine("-----------------------------------");            
            }
        }

        static void GetDevice(ManagementScope scope, string lastUser = null)
        {
            try
            {
                ObjectQuery query = new ObjectQuery();
                if (!string.IsNullOrEmpty(lastUser))
                {
                    query = new ObjectQuery("SELECT * FROM SMS_R_System WHERE LastLogonUserName='" + lastUser + "'");
                }
                else
                {
                    query = new ObjectQuery("SELECT * FROM SMS_R_System");
                }
                ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
                Console.WriteLine("-----------------------------------");
                Console.WriteLine("SMS_R_System instance");
                Console.WriteLine("-----------------------------------");

                foreach (ManagementObject queryObj in searcher.Get())
                {
                    Console.WriteLine("Active: {0}", queryObj["Active"]);

                    if (queryObj["AgentSite"] == null)
                        Console.WriteLine("AgentSite: {0}", queryObj["AgentSite"]);
                    else
                    {
                        String[] arrAgentSite = (String[])(queryObj["AgentSite"]);
                        foreach (String arrValue in arrAgentSite)
                        {
                            Console.WriteLine("AgentSite: {0}", arrValue);
                        }
                    }
                    /*
                    if (queryObj["AgentTime"] == null)
                        Console.WriteLine("AgentTime: {0}", queryObj["AgentTime"]);
                    else
                    {
                        DateTime[] arrAgentTime = (DateTime[])(queryObj["AgentTime"]);
                        foreach (DateTime arrValue in arrAgentTime)
                        {
                            Console.WriteLine("AgentTime: {0}", arrValue);
                        }
                    }
                    */
                    Console.WriteLine("BuildExt: {0}", queryObj["BuildExt"]);
                    Console.WriteLine("Client: {0}", queryObj["Client"]);
                    Console.WriteLine("ClientEdition: {0}", queryObj["ClientEdition"]);
                    Console.WriteLine("ClientType: {0}", queryObj["ClientType"]);
                    Console.WriteLine("ClientVersion: {0}", queryObj["ClientVersion"]);
                    Console.WriteLine("CPUType: {0}", queryObj["CPUType"]);
                    Console.WriteLine("CreationDate: {0}", queryObj["CreationDate"]);
                    Console.WriteLine("Decommissioned: {0}", queryObj["Decommissioned"]);
                    Console.WriteLine("DeviceOwner: {0}", queryObj["DeviceOwner"]);
                    Console.WriteLine("DistinguishedName: {0}", queryObj["DistinguishedName"]);
                    Console.WriteLine("FullDomainName: {0}", queryObj["FullDomainName"]);

                    if (queryObj["IPAddresses"] == null)
                        Console.WriteLine("IPAddresses: {0}", queryObj["IPAddresses"]);
                    else
                    {
                        String[] arrIPAddresses = (String[])(queryObj["IPAddresses"]);
                        foreach (String arrValue in arrIPAddresses)
                        {
                            Console.WriteLine("IPAddresses: {0}", arrValue);
                        }
                    }

                    if (queryObj["IPSubnets"] == null)
                        Console.WriteLine("IPSubnets: {0}", queryObj["IPSubnets"]);
                    else
                    {
                        String[] arrIPSubnets = (String[])(queryObj["IPSubnets"]);
                        foreach (String arrValue in arrIPSubnets)
                        {
                            Console.WriteLine("IPSubnets: {0}", arrValue);
                        }
                    }

                    if (queryObj["IPv6Addresses"] == null)
                        Console.WriteLine("IPv6Addresses: {0}", queryObj["IPv6Addresses"]);
                    else
                    {
                        String[] arrIPv6Addresses = (String[])(queryObj["IPv6Addresses"]);
                        foreach (String arrValue in arrIPv6Addresses)
                        {
                            Console.WriteLine("IPv6Addresses: {0}", arrValue);
                        }
                    }

                    if (queryObj["IPv6Prefixes"] == null)
                        Console.WriteLine("IPv6Prefixes: {0}", queryObj["IPv6Prefixes"]);
                    else
                    {
                        String[] arrIPv6Prefixes = (String[])(queryObj["IPv6Prefixes"]);
                        foreach (String arrValue in arrIPv6Prefixes)
                        {
                            Console.WriteLine("IPv6Prefixes: {0}", arrValue);
                        }
                    }
                    Console.WriteLine("IsAssignedToUser: {0}", queryObj["IsAssignedToUser"]);
                    Console.WriteLine("IsVirtualMachine: {0}", queryObj["IsVirtualMachine"]);
                    Console.WriteLine("LastLogonTimestamp: {0}", queryObj["LastLogonTimestamp"]);
                    Console.WriteLine("LastLogonUserDomain: {0}", queryObj["LastLogonUserDomain"]);
                    Console.WriteLine("LastLogonUserName: {0}", queryObj["LastLogonUserName"]);

                    if (queryObj["MACAddresses"] == null)
                        Console.WriteLine("MACAddresses: {0}", queryObj["MACAddresses"]);
                    else
                    {
                        String[] arrMACAddresses = (String[])(queryObj["MACAddresses"]);
                        foreach (String arrValue in arrMACAddresses)
                        {
                            Console.WriteLine("MACAddresses: {0}", arrValue);
                        }
                    }
                    Console.WriteLine("Name: {0}", queryObj["Name"]);
                    Console.WriteLine("NetbiosName: {0}", queryObj["NetbiosName"]);
                    Console.WriteLine("OperatingSystemNameandVersion: {0}", queryObj["OperatingSystemNameandVersion"]);
                    Console.WriteLine("PrimaryGroupID: {0}", queryObj["PrimaryGroupID"]);
                    Console.WriteLine("ResourceDomainORWorkgroup: {0}", queryObj["ResourceDomainORWorkgroup"]);
                    Console.WriteLine("ResourceId: {0}", queryObj["ResourceId"]);

                    if (queryObj["ResourceNames"] == null)
                        Console.WriteLine("ResourceNames: {0}", queryObj["ResourceNames"]);
                    else
                    {
                        String[] arrResourceNames = (String[])(queryObj["ResourceNames"]);
                        foreach (String arrValue in arrResourceNames)
                        {
                            Console.WriteLine("ResourceNames: {0}", arrValue);
                        }
                    }
                    Console.WriteLine("ResourceType: {0}", queryObj["ResourceType"]);
                    Console.WriteLine("SerialNumber: {0}", queryObj["SerialNumber"]);
                    Console.WriteLine("SID: {0}", queryObj["SID"]);
                    Console.WriteLine("SNMPCommunityName: {0}", queryObj["SNMPCommunityName"]);
                    Console.WriteLine("-----------------------------------");
                }
            }
            catch (ManagementException e)
            {
                Console.WriteLine("An error occurred while querying for WMI data: " + e.Message);
            }
        }
        static void GetPrimaryUser(ManagementScope scope, string device = null, string user = null)
        {
            try
            {
                ObjectQuery query = new ObjectQuery();
                if (!string.IsNullOrEmpty(device))
                {
                    query = new ObjectQuery("SELECT * FROM SMS_UserMachineRelationship WHERE ResourceName='" + device + "'");
                }
                else if (!string.IsNullOrEmpty(user))
                {
                    query = new ObjectQuery("SELECT * FROM SMS_UserMachineRelationship WHERE UniqueUserName LIKE '%" + user + "%'");
                }
                else
                {
                    query = new ObjectQuery("SELECT * FROM SMS_UserMachineRelationship");
                }

                ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, query);
                Console.WriteLine("-----------------------------------");
                Console.WriteLine("SMS_UserMachineRelationship instance");
                Console.WriteLine("-----------------------------------");

                foreach (ManagementObject queryObj in searcher.Get())
                {
                    Console.WriteLine("ResourceName: {0}", queryObj["ResourceName"]);
                    Console.WriteLine("UniqueUserName: {0}", queryObj["UniqueUserName"]);
                    Console.WriteLine("IsActive: {0}", queryObj["IsActive"]);
                    Console.WriteLine("CreationTime: {0}", queryObj["CreationTime"]);
                    Console.WriteLine("-----------------------------------");
                }
            }
            catch (ManagementException err)
            {
                Console.WriteLine("An error occurred while querying for WMI data: " + err.Message);
            }
        }

        static void InvokeQuery(ManagementScope scope, string query)
        {
            try
            {
                ObjectQuery objQuery = new ObjectQuery(query);
              
                ManagementObjectSearcher searcher = new ManagementObjectSearcher(scope, objQuery);
                Console.WriteLine("-----------------------------------");
                Console.WriteLine(objQuery);
                Console.WriteLine("-----------------------------------");

                foreach (ManagementObject queryObj in searcher.Get())
                {
                    foreach(PropertyData prop in queryObj.Properties)
                    {
                        Console.WriteLine("{0}: {1}", prop.Name, prop.Value);
                    }
                    Console.WriteLine("-----------------------------------");
                }
            }
            catch (ManagementException err)
            {
                Console.WriteLine("An error occurred while querying for WMI data: " + err.Message);
            }
        }
        static void Main(string[] args)
        {
            // Gather required arguments
            var rootCommand = new RootCommand();
            rootCommand.Add(new Argument<string>("server", "The FQDN or NetBIOS name of the Configuration Manager server to connect to"));
            rootCommand.Add(new Argument<string>("sitecode", "The site code of the Configuration Manager server (e.g., PS1)"));

            // Subcommands (listed alphabetically)
            var findLocalSccmInfo = new Command("Find-LocalSccmInfo", "Get the primary Management Point and Site Code for the local host");
            rootCommand.Add(findLocalSccmInfo);
            findLocalSccmInfo.Handler = CommandHandler.Create(
                () =>
                {
                    FindLocalSccmInfo();
                });

            // Get-Device options
            var getDevice = new Command("Get-Device", "Get information on devices");
            rootCommand.Add(getDevice);
            getDevice.Add(new Option<string>(new[] { "--last-user", "-u", }, "Get information on devices where a specific user was the last to log in (matches exact string provided)"));
            getDevice.Handler = CommandHandler.Create(
                (string server, string sitecode, string lastUser) =>
                {
                    ManagementScope sccmConnection = NewSccmConnection(server, sitecode);
                    if (!string.IsNullOrEmpty(lastUser)) 
                    {
                        GetDevice(sccmConnection, lastUser);
                    }
                    else
                    {
                        GetDevice(sccmConnection);
                    }
                });

            // Get-PrimaryUser options
            var getPrimaryUser = new Command("Get-PrimaryUser", "Get information on primary users set for devices");
            rootCommand.Add(getPrimaryUser);
            getPrimaryUser.Add(new Option<string>(new[] { "--device", "-d", }, "A specific device to search for (returns the device matching the exact string provided)"));
            getPrimaryUser.Add(new Option<string>(new[] { "--user", "-u", }, "A specific user to search for (returns all devices where the primary user name contains the provided string)"));
            getPrimaryUser.Handler = CommandHandler.Create(
                (string server, string sitecode, string device, string user) =>
                {
                    ManagementScope sccmConnection = NewSccmConnection(server, sitecode);
                    if (!string.IsNullOrEmpty(device))
                    {
                        GetPrimaryUser(sccmConnection, device);
                    }
                    else if (!string.IsNullOrEmpty(user))
                    {
                        GetPrimaryUser(sccmConnection, null, user);
                    }
                    else
                    {
                        GetPrimaryUser(sccmConnection);
                    }
                });

            // Invoke-Query options
            var invokeQuery = new Command("Invoke-Query", "Executes a given WQL query");
            rootCommand.Add(invokeQuery);
            invokeQuery.Add(new Argument<string>("query", "The WQL query to execute"));
            invokeQuery.Handler = CommandHandler.Create(
                (string server, string sitecode, string query) =>
                {
                    ManagementScope sccmConnection = NewSccmConnection(server, sitecode);
                    InvokeQuery(sccmConnection, query);
                });

            // Execute
            rootCommand.Invoke(args);
        }
    }
}
