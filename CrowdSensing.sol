pragma solidity >= 0.8.11 <= 0.8.11;

//smart contract to manage participant details
contract CrowdSensing {
    string public participant_block;
    

    //function to create participant block
    function createParticipantBlock(string memory pb) public {
        participant_block = pb;	
    }

    //function to get participant Block
    function getParticipantBlock() public view returns (string memory) {
        return participant_block;
    }
    
    constructor() public {
        participant_block = "";	
    }
}