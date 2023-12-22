public class VictoryOrDefeat {
  public static final void decisionVictoryOrDefeat(int computerHand, int playerHand) {
    // 課題4 勝敗判定とその表示
    // 課題2,3においてGameMain.javaに実装したPlayerおよびComputerの手の表示は以下に移動する
    System.out.println("プレイヤー : " + Hand.getHandName(playerHand));
    System.out.println("コンピュータ : " + Hand.getHandName(computerHand));

    // int型のplayerHand,computerHandを使って勝敗判定を表示する
    if (playerHand == computerHand) {
      System.out.println("あいこ");
    } else if ((playerHand == 1 && computerHand == 2) || (playerHand == 2 && computerHand == 3)
        || (playerHand == 3 && computerHand == 1)) {
      System.out.println("勝ち");
    } else {
      System.out.println("負け");
    }

  }
}