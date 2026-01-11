// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract PrismIdentity is ERC721, Ownable {
    uint256 private _nextTokenId;
    constructor() ERC721("PrismIdentity", "PRISM") Ownable(msg.sender) {}

    function mintBadge(address to) public onlyOwner {
        uint256 tokenId = _nextTokenId++;
        _safeMint(to, tokenId);
    }
    // Soulbound: Disable transfers
    function transferFrom(address, address, uint256) public pure override {
        revert("Soulbound: Transfer failed");
    }
}