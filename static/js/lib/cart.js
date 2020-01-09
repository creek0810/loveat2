/* eslint-disable no-underscore-dangle */
/* eslint-disable no-unused-vars */
/* global FetchData */

/**
 * @description do operating at local storage
 *
 * @class Cart
 */
class Cart {
  constructor() {
    return (async () => {
      this.prefix = 'loveat2-cart';
      if (this.prefix in localStorage) {
        this.content = JSON.parse(localStorage.getItem(this.prefix));
        const itemList = [];
        const comboList = [];
        Object.keys(this.content).forEach((key) => {
          if (this.content[key].category === 'item') {
            itemList.push(key);
          } else {
            comboList.push(key);
          }
        });
        const itemResult = await FetchData.post(
          '/api/menu/item',
          itemList,
        ).then((res) => res.json());
        const comboResult = await FetchData.post(
          '/api/menu/combo',
          comboList,
        ).then((res) => res.json());
        itemResult.forEach((cur) => {
          this.content[cur._id].price = cur.price;
          this.content[cur._id].name = cur.name;
        });
        comboResult.forEach((cur) => {
          this.content[cur._id].price = cur.price;
          this.content[cur._id].name = cur.name;
        });
      } else {
        this.content = {};
      }
      return this;
    })();
  }

  /**
   * @description update the order which key is loveat2-cart
   *
   * @memberof Cart
   */
  updateLocalStorage() {
    localStorage.setItem(this.prefix, JSON.stringify(this.content));
  }

  /**
   *@description check item quantity if it is not over 99
   *
   * @param {*} data
   * @returns
   * @memberof Cart
   */
  checkAndSetQuantity(dataId, quantity) {
    const nowQuantity = this.content[dataId].quantity;
    const totalQuantity = nowQuantity + quantity;
    if (totalQuantity <= 99) {
      this.content[dataId].quantity = totalQuantity;
      return true;
    }
    this.content[dataId].quantity = 99;
    return false;
  }

  /**
   * @description add the item quantity which key is loveat2-cart
   *
   * @param {*} data
   * @memberof Cart
   */
  add(data) {
    let addResult = true;
    if (data._id in this.content) {
      addResult = this.checkAndSetQuantity(data._id, data.quantity);
    } else {
      this.content[data._id] = {
        category: data.category,
        quantity: data.quantity,
        description: '',
      };
    }
    this.updateLocalStorage();
    return addResult;
  }

  /**
   * @description get order form local storage
   *
   * @returns
   * @memberof Cart
   */
  get() {
    return this.content;
  }

  /**
   * @description delete the target item by key
   *
   * @param {*} key index of deleting item
   * @memberof Cart
   */
  delete(key) {
    delete this.content[key];
    this.updateLocalStorage();
  }

  /**
   * @description remove the item which key is loveat2-cart
   *
   * @memberof Cart
   */
  clear() {
    localStorage.removeItem(this.prefix);
  }

  /**
   *@description update item quantity
   *
   * @param {*} id
   * @param {*} quantity
   * @memberof Cart
   */
  updateQuantity(id, quantity) {
    this.content[id].quantity = quantity;
    this.updateLocalStorage();
  }
}
