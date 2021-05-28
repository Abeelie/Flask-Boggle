class BoggleGame {
  constructor(boardId, seconds) {
    this.seconds = seconds; 
    this.showTimer();
    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);
    this.timer = setInterval(this.countDown.bind(this), 1000);

    $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
  }

  async handleSubmit(evt) {
    evt.preventDefault();
    const $word = $(".word", this.board);

    let word = $word.val();
    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`, "err");
      return;
    }

    const resp = await axios.get("/check-word", { params: { word: word }});
    if (resp.data.result === "not-word") {
      this.showMessage(`${word} is not a valid English word`, "err");
    } else if (resp.data.result === "not-on-board") {
      this.showMessage(`${word} is not a valid word on this board`, "err");
    } else {
      this.showWord(word);
      this.score += word.length;
      this.showScore();
      this.words.add(word);
      this.showMessage(`Added: ${word}`, "ok");
    }

    $word.val("");
  }

  showTimer() {
    $(".timer", this.board).text(this.seconds);
  }

  async countDown() {
    this.seconds -= 1;
    this.showTimer();

    if (this.seconds === 0) {
      clearInterval(this.timer);
      await this.endGame();
    }
  }

  showScore() {
    $(".score", this.board).text(this.score);
  }

  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }

  showMessage(msg) {
    $(".msg", this.board).text(msg);
  }

  async endGame() {
    $(".add-word", this.board).hide();
    const resp = await axios.post("/post-score", { score: this.score });
    if (resp.data.brokeRecord) {
      this.showMessage(`New record: ${this.score}`, "ok");
    } else {
      this.showMessage(`Final score: ${this.score}`, "ok");
    }
  }
}