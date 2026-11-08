// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title Nexus QDAG Protocol Sovereign Token ($NXQ)
 * @dev Post-Quantum Inspired Parallel Mesh Asset
 * Standard: ERC-20 / BEP-20
 * Max Supply: 2,100,000 NXQ (10x rarer than Bitcoin)
 * Arsitek: Made Suke Raditia
 */
contract NexusToken {
    string public constant name = "Nexus QDAG Protocol";
    string public constant symbol = "NXQ";
    uint8 public constant decimals = 18;
    uint256 public constant MAX_SUPPLY = 2_100_000 * 10**18;
    
    uint256 public totalSupply;
    address public owner;
    
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
    event Burn(address indexed from, uint256 value);

    modifier onlyOwner() {
        require(msg.sender == owner, "Only protocol founder");
        _;
    }

    constructor() {
        owner = msg.sender;
        uint256 founderReserve = 210_000 * 10**18;
        uint256 publicPool = MAX_SUPPLY - founderReserve;
        
        _mint(owner, founderReserve);
        _mint(address(this), publicPool);
    }

    function _mint(address to, uint256 amount) internal {
        require(totalSupply + amount <= MAX_SUPPLY, "Exceeds Max Supply");
        totalSupply += amount;
        balanceOf[to] += amount;
        emit Transfer(address(0), to, amount);
    }

    // FUNGSI AUDIT: Melepaskan koin alokasi presale/mining secara resmi
    function releasePresaleTokens(address recipient, uint256 amount) external onlyOwner {
        require(recipient != address(0), "Invalid recipient");
        require(balanceOf[address(this)] >= amount, "Insufficient contract pool");

        balanceOf[address(this)] -= amount;
        balanceOf[recipient] += amount;
        emit Transfer(address(this), recipient, amount);
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        _transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(allowance[from][msg.sender] >= amount, "Allowance exceeded");
        allowance[from][msg.sender] -= amount;
        _transfer(from, to, amount);
        return true;
    }

    function _transfer(address from, address to, uint256 amount) internal {
        require(to != address(0), "Transfer to zero address");
        require(balanceOf[from] >= amount, "Insufficient balance");

        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
    }

    function burn(uint256 amount) public {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
        emit Burn(msg.sender, amount);
        emit Transfer(msg.sender, address(0), amount);
    }
}
