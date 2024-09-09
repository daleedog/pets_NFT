// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";  // Foundry's Script library
import "../src/NFTMinter.sol";   // Import the NFTMinter contract

contract DeployNFTMinter is Script {
    function run() external {
        vm.startBroadcast();  // Start broadcasting transactions (deployment)

        // Deploy the contract
        nftMinter nftMinterContract = new nftMinter();

        // Optional: Log the deployed contract address
        console.log("NFTMinter deployed at:", address(nftMinterContract));

        vm.stopBroadcast();  // Stop broadcasting transactions
    }
}
