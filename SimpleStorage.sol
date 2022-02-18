// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

contract SimpleStorage {
    uint256 favNum; // by default initialised to null

    struct People {
        uint256 favNum;
        string name;
    }

    // People public person = People({favNum: 5, name: "Virat"});

    People[] public person;
    mapping(string => uint256) public nameTofavNum;

    function store(uint256 _favNum) public returns(uint256){
        favNum = _favNum;
        return favNum;
    }

    // view function states that we want to read some state of the blockchain
    function retrieve() public view returns (uint256) {
        return favNum;
    }

    function addPerson(string memory _name, uint256 _favNum) public {
        person.push(People({favNum: _favNum, name: _name}));
        nameTofavNum[_name] = _favNum;
    }
}
