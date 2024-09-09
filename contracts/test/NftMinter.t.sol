// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol"; // Foundry's standard library for testing
import "../src/NFTMinter.sol"; // Path to your contract file

contract NFTMinterTest is Test {
    nftMinter private nftMinterContract;
    address private owner;
    address private user;

    function setUp() public {
        // Deploy the contract
        owner = address(this); // Test contract as the owner
        user = address(0x1); // Sample user address
        nftMinterContract = new nftMinter();

        // Optional: Label addresses for better readability in Foundry traces
        vm.label(owner, "Owner");
        vm.label(user, "User");
    }

    function testMintNFT() public {
        // Arrange
        string memory tokenURI = "https://example.com/token-metadata.json";
        bytes32 userHash = keccak256(abi.encodePacked(user));

        // Act
        uint256 newItemId = nftMinterContract.mintNFT(tokenURI, userHash);

        // Assert
        assertEq(newItemId, 0); // First minted ID should be 0
        assertEq(nftMinterContract.getItemId(), 1); // Check if the ID counter has incremented
        assertEq(nftMinterContract.ownerOf(newItemId), owner); // Ensure the owner is correct
    }

    function testTransferToUserAddress() public {
        // Arrange
        string memory tokenURI = "https://example.com/token-metadata.json";
        bytes32 userHash = keccak256(abi.encodePacked(user));
        nftMinterContract.mintNFT(tokenURI, userHash);

        // Act
        nftMinterContract.transfer_to_user_address(userHash, user);

        // Assert
        assertEq(nftMinterContract.ownerOf(0), user); // Ensure the NFT was transferred correctly
    }

    function testFailMintNFTNonOwner() public {
        // Arrange
        vm.prank(user); // Impersonate a non-owner address
        string memory tokenURI = "https://example.com/token-metadata.json";
        bytes32 userHash = keccak256(abi.encodePacked(user));

        // Act & Assert: Should revert because mintNFT is restricted to owner
        nftMinterContract.mintNFT(tokenURI, userHash);
    }

    function testFailTransferToUserAddressInvalidUser() public {
        // Arrange
        string memory tokenURI = "https://example.com/token-metadata.json";
        bytes32 userHash = keccak256(abi.encodePacked(user));
        nftMinterContract.mintNFT(tokenURI, userHash);

        // Act & Assert: Attempt to transfer to address(0), which should fail
        vm.expectRevert(); // Expect revert due to invalid address
        nftMinterContract.transfer_to_user_address(userHash, address(0));
    }
}
