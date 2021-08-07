using System;
using System.CommandLine;
using System.CommandLine.Invocation;
using System.Management;
namespace SharpSCCM
{
    static class Program
    {
        static ManagementScope GetSccmConnection(string server, string sitecode)
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
        static void GetPrimaryUser(ManagementScope scope)
        {
            try
            {
                ObjectQuery query = new ObjectQuery("SELECT * FROM SMS_UserMachineRelationship");
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
        static void Main(string[] args)
        {
            /*
            string server = "atlas.aperture.science";
            string sitecode = "PS1";
            ManagementScope scope = GetSccmConnection(server, sitecode);
            */
            // Gather required arguments
            var rootCommand = new RootCommand();
            rootCommand.Add(new Argument<string>("server", "The FQDN or NetBIOS name of the Configuration Manager server to connect to"));
            rootCommand.Add(new Argument<string>("sitecode", "The site code of the Configuration Manager server (e.g., PS1)"));
            rootCommand.Handler = CommandHandler.Create(
                (string server, string sitecode) =>
                {
                    ManagementScope scope = GetSccmConnection(server, sitecode);
                });
            // Subcommands
            // Get-PrimaryUser
            var getPrimaryUser = new Command("Get-PrimaryUser", "Returns information on primary users set for devices");
            rootCommand.Add(getPrimaryUser);
            getPrimaryUser.Add(new Option<string>(new[] { "--device", "-d", }, "A specific device to search for"));
            getPrimaryUser.Handler = CommandHandler.Create(
                () =>
                {
                    GetPrimaryUser(scope);
                });

            // Execute
            rootCommand.Invoke(args);
        }
    }
}
