public class Hand {
  public static final int GU = 1;
  public static final int CHOKI = 2;
  public static final int PA = 3;

  public static String getHandName(int hand) {
    String handName = "";

    // 課題2 Playerの手の決定とその表示
    // 1ならば"グー",2ならば"チョキ",3ならば"パー"を返す
    if (hand == GU)
      handName = "グー";
    else if (hand == CHOKI)
      handName = "チョキ";
    else if (hand == PA)
      handName = "パー";

    return handName;
  }
}