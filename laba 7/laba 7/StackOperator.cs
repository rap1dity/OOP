using System;
using System.Collections;
using System.Collections.Generic;

namespace MyApp
{
    internal static class StatisticOperation
    {
        public static void PopAtIndex(this CollectionType<Production> collection, int index)
        {
            if (index >= collection.Count || index < 0)
                throw new ArgumentOutOfRangeException(nameof(index));

            var auxiliaryStack = new CollectionType<Production>();

            for (int i = 0; i < index; i++)
                auxiliaryStack.Push(collection.Pop());

            var poppedItem = collection.Pop();

            for (int i = 0; i < index; i++)
                collection.Push(auxiliaryStack.Pop());
        }
    }
}