// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract nftMinter is ERC721URIStorage ,Ownable {

    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;
    mapping(bytes32 => unit256) private _user_to_item;


    constructor() ERC721("PET NFT", "PET") Ownable(msg.sender) {}

    function mintNFT(string memory tokenURI, bytes32 user_hash) public onlyOwner returns (uint256) {
        uint256 newItemId = _tokenIds.current();
        _mint(msg.sender, newItemId);
        _setTokenURI(newItemId, tokenURI);
        _user_to_item[user_hash] = newItemId;
        _tokenIds.increment();
        return newItemId;
    }

    function getItemId() public view returns(uint256) {
        uint256 id = _tokenIds.current();
        return id;
    }

    function transfer_to_user_address(bytes32 user_hash, address user_address) public onlyOwner {
        require(user_address != address(0));
        uint256 user_item = _user_to_item[user_hash];
        require(user_item != 0);
        approve(user_address, user_item);
        transferFrom(msg.sender, user_address, user_item);
        delete _user_to_item[user_hash];
    }

}