public class GameMain {
  public static void main(String[] args) {
    int playerHand;
    // 課題1 文章の表示
    System.out.println("1:グー 2:チョキ 3:パー");
    System.out.println("じゃんけん...");

    // 課題2 Playerの手の決定とその表示
    // HandクラスのgetHandNameメソッドを使ってPlayerの手を表示する
    if (args.length == 1) {
      playerHand = Integer.parseInt(args[0]);
    } else {
      System.out.println("コマンドライン引数でプレイヤーの手を決定して下さい");
      return;
    }
    System.out.println("プレイヤー : " + Hand.getHandName(playerHand));

    // 課題3 Computerの手の決定とその表示
    // ComputerクラスのdecidesComputerHandメソッドとHandクラスのgetHandNameメソッドを使ってPlayerの手を表示する


    // 課題4 勝敗判定とその表示
    // 課題2,3において実装したPlayerおよびComputerの手の表示はVictoryOrDefeatクラスに移動する

  }
}