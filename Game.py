import random

class Domino:
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __repr__(self):
        return f"[{self.left}|{self.right}]"

class Node:
    def __init__(self, domino):
        self.domino = domino
        self.prev = None
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_end(self, domino):
        new_node = Node(domino)
        if not self.tail:  # 链表为空
            self.head = self.tail = new_node
        else:  # 添加到链表尾部
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def add_to_start(self, domino):
        new_node = Node(domino)
        if not self.head:  # 链表为空
            self.head = self.tail = new_node
        else:  # 添加到链表头部
            self.head.prev = new_node
            new_node.next = self.head
            self.head = new_node

    def __str__(self):
        result = []
        current = self.head
        while current:
            result.append(str(current.domino))
            current = current.next
        return " <-> ".join(result)

class CubanDominoGame:
    def __init__(self):
        self.dominoes = [Domino(i, j) for i in range(10) for j in range(i, 10)]
        self.table = LinkedList()
        self.player_hand = []
        self.computer_hand = []

    def shuffle(self):
        random.shuffle(self.dominoes)

    def deal(self):
        for _ in range(10):
            self.player_hand.append(self.dominoes.pop())
            self.computer_hand.append(self.dominoes.pop())

    def place_first_domino(self):
        domino = self.dominoes.pop(0)
        self.table.add_to_end(domino)

    def can_play(self, domino, to_start=False):
        if to_start:
            return self.table.head and domino.right == self.table.head.domino.left
        else:
            return self.table.tail and domino.left == self.table.tail.domino.right

    def play_domino(self, hand, domino, to_start=False):
        if self.can_play(domino, to_start):
            if to_start:
                self.table.add_to_start(domino)
            else:
                self.table.add_to_end(domino)
            hand.remove(domino)
            return True
        return False

    def calculate_score(self, hand):
        return sum(domino.left + domino.right for domino in hand)

    def __str__(self):
        return str(self.table)

def main():
    game = CubanDominoGame()
    game.shuffle()
    game.deal()
    game.place_first_domino()

    print("Initial Table:")
    print(game)

    player_turn = True  # 玩家先手

    # 无法出牌的回合计数
    consecutive_passes = 0

    while True:
        print("\nCurrent Table:", game)

        if player_turn:
            print("\nYour hand:", game.player_hand)
            valid_moves = [
                domino for domino in game.player_hand
                if game.can_play(domino, to_start=True) or game.can_play(domino, to_start=False)
            ]
            if not valid_moves:
                print("You have no valid moves!")
                consecutive_passes += 1
                player_turn = False
                if consecutive_passes >= 2:  # 双方都无法出牌
                    break
                continue

            consecutive_passes = 0  # 玩家出牌成功，重置计数

            while True:
                try:
                    print("Choose a domino to play (index):")
                    for i, domino in enumerate(valid_moves):
                        print(f"{i}: {domino}")
                    index = int(input("Enter the index of the domino: "))
                    if index < 0 or index >= len(valid_moves):
                        raise ValueError("Invalid index.")
                    selected_domino = valid_moves[index]
                    break
                except ValueError as e:
                    print("Invalid input. Please enter a valid index.")

            can_play_left = game.can_play(selected_domino, to_start=True)
            can_play_right = game.can_play(selected_domino, to_start=False)

            if can_play_left and can_play_right:
                while True:
                    side = input("Place on the left or right? (l/r): ").strip().lower()
                    if side == 'l':
                        success = game.play_domino(game.player_hand, selected_domino, to_start=True)
                        break
                    elif side == 'r':
                        success = game.play_domino(game.player_hand, selected_domino, to_start=False)
                        break
                    else:
                        print("Invalid input. Please enter 'l' or 'r'.")
            elif can_play_left:
                print("Automatically placing on the left.")
                success = game.play_domino(game.player_hand, selected_domino, to_start=True)
            elif can_play_right:
                print("Automatically placing on the right.")
                success = game.play_domino(game.player_hand, selected_domino, to_start=False)
            else:
                print("Unexpected error: the selected domino cannot be placed.")
                continue

            if success:
                print(f"You played: {selected_domino}")
        else:
            print("\nComputer's turn.")
            valid_moves = [
                domino for domino in game.computer_hand
                if game.can_play(domino, to_start=True) or game.can_play(domino, to_start=False)
            ]
            if not valid_moves:
                print("Computer has no valid moves!")
                consecutive_passes += 1
                player_turn = True
                if consecutive_passes >= 2:  # 双方都无法出牌
                    break
                continue

            consecutive_passes = 0  # 电脑出牌成功，重置计数

            # 简单的AI逻辑：优先选择点数最大的牌
            selected_domino = max(valid_moves, key=lambda d: d.left + d.right)
            if game.can_play(selected_domino, to_start=True):
                game.play_domino(game.computer_hand, selected_domino, to_start=True)
            else:
                game.play_domino(game.computer_hand, selected_domino, to_start=False)

            print(f"Computer played: {selected_domino}")

        # 检查游戏结束条件
        if not game.player_hand or not game.computer_hand:
            break

        # 切换回合
        player_turn = not player_turn

    # 计算分数
    player_score = game.calculate_score(game.player_hand)
    computer_score = game.calculate_score(game.computer_hand)
    print("\nGame Over!")
    print(f"Your remaining tiles: {game.player_hand} (Score: {player_score})")
    print(f"Computer's remaining tiles: {game.computer_hand} (Score: {computer_score})")

    if player_score < computer_score:
        print("You win!")
    elif player_score > computer_score:
        print("Computer wins!")
    else:
        print("It's a tie!")

if __name__ == "__main__":
    main()
