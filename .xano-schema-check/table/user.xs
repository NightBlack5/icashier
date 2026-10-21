// Stores user information and allows the user to authenticate  against
table user {
  auth = true

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text name filters=trim
    email? email filters=trim|lower
    password? password filters=min:8|minAlpha:1|minDigit:1 {
      visibility = "internal"
    }
  
    // Reference to the company the user belongs to.
    int account_id? {
      table = "account"
    }
  
    // The role of the user within their company (e.g., 'admin', 'member').
    enum role? {
      values = ["admin", "member"]
      visibility = "private"
    }
  
    object password_reset? {
      schema {
        password token? {
          visibility = "internal"
        }
      
        timestamp? expiration? {
          visibility = "internal"
        }
      
        bool used? {
          visibility = "internal"
        }
      }
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree|unique", field: [{name: "email", op: "asc"}]}
  ]

  tags = ["xano:quick-start"]
  guid = "g8tpjso2orFaPgdxKGzuuR66M1k"
  items = [
    {
      id            : 2
      created_at    : 1791322326207
      name          : "Conta de Teste CashSave"
      email         : "cashsave-test-1791322325983@example.com"
      password      : "c1ffe00ad05f9a76.7affad1737de37e185288ec321edccf26bc9708f8315ab26e59f2da2420746e8"
      account_id    : 0
      role          : "member"
      password_reset: {used: false, token: "", expiration: null}
    }
    {
      id            : 4
      created_at    : 1792447823469
      name          : "Eduardo Fonseca"
      email         : "eduardo.fonseca@aluno.impacta.edu.br"
      password      : "d7d81a90a08c279c.0013b59403a0daaf4420dbde03b7cf6d2f8e7158f23fa4f4d676b8a13bd3d388"
      account_id    : 0
      role          : "member"
      password_reset: {used: false, token: "", expiration: null}
    }
    {
      id            : 5
      created_at    : 1792450024738
      name          : "Gabriel Caitano"
      email         : "gabriel.caitano@icloud.com"
      password      : "9b6e67782dfdd59f.e084b1c51452ab737d31a4fab105b25af85b8e34a83cc6ee536714b804362bd9"
      account_id    : 0
      role          : "member"
      password_reset: {used: false, token: "", expiration: null}
    }
    {
      id            : 6
      created_at    : 1792451597775
      name          : "Fernando Fernandes Santos"
      email         : "fernandofernandessantos123@gmail.com"
      password      : "f7d5c8aed852877a.41965312307fa5691dc2cc2e96f2550717aab8757d82423bdc372d2e879ec80a"
      account_id    : 0
      role          : "member"
      password_reset: {used: false, token: "", expiration: null}
    }
  ]
}